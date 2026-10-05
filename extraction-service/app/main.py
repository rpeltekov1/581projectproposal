import hashlib, os, secrets, uuid, time
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import text
from . import database as db
from .extractor import extract, ConfigurationError, PROMPT_VERSION

@asynccontextmanager
async def lifespan(app):
    db.initialize()
    yield
app=FastAPI(title='Parcel Floor-Plan Extraction',version='0.1.0',lifespan=lifespan)
security=HTTPBearer(auto_error=False)
def service_auth(credentials:HTTPAuthorizationCredentials|None=Depends(security)):
    expected=os.getenv('SERVICE_TOKEN','')
    if not expected or not credentials or not secrets.compare_digest(credentials.credentials,expected):
        raise HTTPException(401,'Service authentication required')

@app.get('/health',dependencies=[Depends(service_auth)])
def health():
    with db.Session() as s:s.execute(text('SELECT 1'))
    return {'status':'ok','vision_configured':bool(os.getenv('VISION_API_KEY') and os.getenv('VISION_MODEL')),'version':'0.1.0'}

@app.post('/v1/extract',dependencies=[Depends(service_auth)])
async def extract_plan(file:UploadFile=File(...),run_id:str=Form(...)):
    try:uuid.UUID(run_id)
    except ValueError:raise HTTPException(422,'run_id must be a UUID')
    # Bounded read; reject over-limit uploads before decoding.
    raw=await file.read(10*1024*1024+1)
    sha=hashlib.sha256(raw).hexdigest();started=time.monotonic()
    root=Path(os.getenv('UPLOAD_DIR','/data/plans'));root.mkdir(parents=True,exist_ok=True)
    path=root/(run_id+'.bin')
    with db.Session() as s:
        previous=s.get(db.ExtractionRun,run_id)
        if previous:
            if previous.source_sha256!=sha:raise HTTPException(409,'run_id already belongs to another source')
            if previous.status=='completed':return {'result':previous.result,'provenance':previous.provenance}
            raise HTTPException(409,'Run already exists; retry with a new run_id')
        record=db.ExtractionRun(id=run_id,source_sha256=sha,status='running',filename=(file.filename or 'plan')[:200],source_path=str(path),provenance={'prompt_version':PROMPT_VERSION,'source_sha256':sha,'service_revision':os.getenv('SERVICE_REVISION','local-unversioned')})
        s.add(record);s.commit()
    try:
        if not raw or len(raw)>10*1024*1024:raise ValueError('File size must be 1 byte to 10 MB')
        path.write_bytes(raw);path.chmod(0o600)
        output=await extract(raw)
        provenance={**output['provenance'],'duration_ms':round((time.monotonic()-started)*1000),'run_id':run_id}
        with db.Session() as s:
            record=s.get(db.ExtractionRun,run_id);record.status='completed';record.result=output['result'];record.provenance=provenance;record.raw_response=output['raw_response'];record.completed=db.now();s.commit()
        return {'result':output['result'],'provenance':provenance}
    except Exception as exc:
        # Store diagnostic class, never provider request headers or secrets.
        message=str(exc) if isinstance(exc,(ValueError,ConfigurationError)) else type(exc).__name__
        with db.Session() as s:
            record=s.get(db.ExtractionRun,run_id);record.status='failed';record.error=message[:2000];record.completed=db.now();record.provenance={**record.provenance,'duration_ms':round((time.monotonic()-started)*1000)};s.commit()
        raise HTTPException(503 if isinstance(exc,ConfigurationError) else 422,{'run_id':run_id,'error':message})
