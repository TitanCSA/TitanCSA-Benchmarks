"""Synthetic unit fixtures only: never exported into benchmark datasets."""
import json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import analyze
class ValidationTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.original=analyze.ROOT;analyze.ROOT=self.root;self.run=self.root/'fixture';self.run.mkdir()
  (self.run/'run.json').write_text(json.dumps({'run_id':'unit-fixture-only','samples':3,'warmup':1,'requested_hz':1000,'seed':1,'qpc_frequency':1000000,'version':'fixture','utc':'2026-11-17'}))
  (self.run/'orchestration.json').write_text('{"status":"completed"}')
  (self.run/'submission.csv').write_text('sequence,submit_qpc,return_qpc,error\n0,100,101,0\n1,200,202,0\n2,300,303,0\n3,400,404,0\n')
  self.rx='sequence,submit_qpc,receive_qpc,content_valid\n0,100,110,1\n1,200,220,1\n2,300,330,1\n3,400,440,1\n';(self.run/'reception.csv').write_text(self.rx)
 def tearDown(self):analyze.ROOT=self.original;self.temp.cleanup()
 def test_warmup_and_known_quantiles(self):
  r=analyze.analyze(self.run);self.assertEqual(r['status'],'measured');self.assertEqual(r['received'],3);self.assertAlmostEqual(r['p50_us'],30);self.assertAlmostEqual(r['p99_us'],39.8)
 def test_clock_reversal_rejected(self):
  (self.run/'reception.csv').write_text(self.rx.replace('2,300,330','2,300,299'));self.assertEqual(analyze.analyze(self.run)['status'],'invalid')
 def test_bad_content_rejected(self):
  (self.run/'reception.csv').write_text(self.rx.replace('2,300,330,1','2,300,330,0'));self.assertEqual(analyze.analyze(self.run)['status'],'invalid')
 def test_duplicate_rejected(self):
  (self.run/'reception.csv').write_text(self.rx+'2,300,331,1\n');self.assertEqual(analyze.analyze(self.run)['status'],'invalid')
 def test_missing_is_counted_not_hidden(self):
  (self.run/'reception.csv').write_text(self.rx.replace('2,300,330,1\n',''));r=analyze.analyze(self.run);self.assertEqual(r['status'],'measured');self.assertEqual(r['missing'],1)
 def test_incomplete_run_rejected(self):
  (self.run/'orchestration.json').unlink();self.assertEqual(analyze.analyze(self.run)['status'],'invalid')
 def test_crash_truncated_metadata_is_invalid(self):
  (self.run/'run.json').write_text('');self.assertEqual(analyze.analyze(self.run)['status'],'invalid')
 def test_explicit_invalidation_is_retained(self):
  (self.run/'invalidated.json').write_text('{"reason":"confounded unit fixture"}');self.assertEqual(analyze.analyze(self.run)['reason'],'confounded unit fixture')
 def test_crash_corrupted_csv_is_invalid(self):
  (self.run/'reception.csv').write_bytes(b'\x00'*256);self.assertEqual(analyze.analyze(self.run)['status'],'invalid')
if __name__=='__main__':unittest.main()
