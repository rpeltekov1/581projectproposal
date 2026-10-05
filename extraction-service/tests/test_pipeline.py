import asyncio, copy, json, os, tempfile, unittest, uuid
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.schema import Layout
from app.extractor import extract, prepare_document, parse_tagged_text, ConfigurationError
from app.scoring import score
from app.main import app
from app import database as db
ROOT=Path(__file__).resolve().parents[1]
KEY=json.loads((ROOT/'fixtures/answer-key.json').read_text())

class ScoringTests(unittest.TestCase):
    def test_perfect_and_unknown(self):
        key=Layout.model_validate(KEY);self.assertEqual(score(key,key)['count_accuracy'],1)
        pred=copy.deepcopy(KEY);pred['doors']=None
        self.assertEqual(score(Layout.model_validate(pred),key)['count_accuracy'],.75)
    def test_area_units_and_basis(self):
        pred=copy.deepcopy(KEY);pred['unit']='sqm';pred['total_area']/=10.76391041671
        for r in pred['rooms']:r['area']/=10.76391041671
        self.assertAlmostEqual(score(Layout.model_validate(pred),Layout.model_validate(KEY))['total_area_relative_error'],0)
        pred['area_basis']='gross';self.assertIsNone(score(Layout.model_validate(pred),Layout.model_validate(KEY))['total_area_relative_error'])
    def test_duplicate_ids_rejected(self):
        pred=copy.deepcopy(KEY);pred['rooms'][1]['id']='r1'
        with self.assertRaises(ValueError):Layout.model_validate(pred)
    def test_missing_room_penalized(self):
        pred=copy.deepcopy(KEY);pred['rooms'].pop()
        self.assertEqual(score(Layout.model_validate(pred),Layout.model_validate(KEY))['room_recall'],5/6)

class ExtractorTests(unittest.TestCase):
    def test_tagged_pdf_no_model(self):
        out=asyncio.run(extract((ROOT/'fixtures/tagged.pdf').read_bytes()))
        self.assertEqual(out['result']['doors'],7);self.assertEqual(out['provenance']['method'],'tagged-text-v1')
    def test_labelled_and_bare_need_vision(self):
        with patch.dict(os.environ,{'VISION_API_KEY':'','VISION_MODEL':''}):
            for name in ['labelled','bare']:
                with self.assertRaises(ConfigurationError):asyncio.run(extract((ROOT/f'fixtures/{name}.pdf').read_bytes()))
    def test_bad_file(self):
        with self.assertRaises(ValueError):prepare_document(b'not a plan')
    def test_incomplete_text_not_assumed_complete(self):
        self.assertIsNone(parse_tagged_text('BEDROOMS: 2\nBATHROOMS: 1'))

class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();p=Path(cls.tmp.name)
        cls.env=patch.dict(os.environ,{'DATABASE_URL':f'sqlite:///{p}/tests.db','DB_AUTO_CREATE':'1','UPLOAD_DIR':str(p/'plans'),'SERVICE_TOKEN':'test-service-secret','VISION_API_KEY':'','VISION_MODEL':''});cls.env.start()
        cls.client=TestClient(app);cls.client.__enter__();cls.headers={'Authorization':'Bearer test-service-secret'}
    @classmethod
    def tearDownClass(cls):
        cls.client.__exit__(None,None,None);cls.env.stop();cls.tmp.cleanup()
    def test_auth_required(self):self.assertEqual(self.client.get('/health').status_code,401)
    def test_success_and_idempotency(self):
        rid=str(uuid.uuid4());payload={'files':{'file':('plan.pdf',(ROOT/'fixtures/tagged.pdf').read_bytes())},'data':{'run_id':rid},'headers':self.headers}
        first=self.client.post('/v1/extract',**payload);self.assertEqual(first.status_code,200,first.text)
        second=self.client.post('/v1/extract',**payload);self.assertEqual(first.json(),second.json())
        different=self.client.post('/v1/extract',headers=self.headers,files={'file':('bad.pdf',b'other')},data={'run_id':rid});self.assertEqual(different.status_code,409)
    def test_failed_run_is_logged(self):
        rid=str(uuid.uuid4());r=self.client.post('/v1/extract',headers=self.headers,files={'file':('bad.pdf',b'bad')},data={'run_id':rid});self.assertEqual(r.status_code,422)
        with db.Session() as s:self.assertEqual(s.get(db.ExtractionRun,rid).status,'failed')
    def test_unconfigured_vision_is_not_fake_success(self):
        rid=str(uuid.uuid4());r=self.client.post('/v1/extract',headers=self.headers,files={'file':('bare.pdf',(ROOT/'fixtures/bare.pdf').read_bytes())},data={'run_id':rid});self.assertEqual(r.status_code,503)
        with db.Session() as s:
            run=s.get(db.ExtractionRun,rid);self.assertIsNone(run.result);self.assertEqual(run.status,'failed')
if __name__=='__main__':unittest.main()
