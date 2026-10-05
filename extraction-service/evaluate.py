"""Run a frozen manifest. Answer keys are loaded only AFTER the service returns."""
import argparse, hashlib, json, os, uuid
from pathlib import Path
import httpx
from app.schema import Layout
from app.scoring import score

def digest(raw):return hashlib.sha256(raw).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('manifest',type=Path);p.add_argument('--service',default='http://127.0.0.1:8000');p.add_argument('--output',type=Path,default=Path('evaluation-report.json'));a=p.parse_args()
    manifest_raw=a.manifest.read_bytes();manifest=json.loads(manifest_raw);root=a.manifest.parent
    if not manifest['cases']:raise SystemExit('Manifest contains no cases')
    result={'manifest_sha256':digest(manifest_raw),'test_set_id':manifest['test_set_id'],'synthetic':manifest.get('synthetic',False),'cases':[]}
    for case in manifest['cases']:
        source=(root/case['file']).read_bytes();key_bytes=(root/case['answer_key']).read_bytes()
        if digest(source)!=case['sha256'] or digest(key_bytes)!=case['key_sha256']:raise SystemExit('Hash mismatch: '+case['id'])
        run_id=str(uuid.uuid4())
        # Only source bytes are sent to extraction; no key or expected values.
        try:
            response=httpx.post(a.service+'/v1/extract',headers={'Authorization':'Bearer '+os.environ['SERVICE_TOKEN']},files={'file':(case['file'],source)},data={'run_id':run_id},timeout=60)
            response.raise_for_status();out=response.json()
            metrics=score(Layout.model_validate(out['result']),Layout.model_validate_json(key_bytes))
            result['cases'].append({'id':case['id'],'tier':case['tier'],'run_id':run_id,'status':'completed','metrics':metrics,'provenance':out['provenance']})
        except Exception as exc:
            result['cases'].append({'id':case['id'],'tier':case['tier'],'run_id':run_id,'status':'failed','error':type(exc).__name__})
        a.output.write_text(json.dumps(result,indent=2))
    result['coverage']=sum(c['status']=='completed' for c in result['cases'])/len(result['cases'])
    # Failures score zero in aggregate, so difficult plans cannot disappear.
    result['failure_inclusive_count_accuracy']=sum((c.get('metrics',{}).get('count_accuracy') or 0) for c in result['cases'])/len(result['cases'])
    a.output.write_text(json.dumps(result,indent=2));print(a.output)
if __name__=='__main__':main()
