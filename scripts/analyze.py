"""Validate raw runs before generating statistics. Never synthesize samples."""
from pathlib import Path
import csv,hashlib,json,statistics
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def rows(path):
    with path.open(newline='',encoding='utf-8-sig') as f:return [{k:int(v) for k,v in row.items()} for row in csv.DictReader(f)]
def analyze(path):
    try:cfg=json.loads((path/'run.json').read_text(encoding='utf-8-sig'))
    except ValueError:return {'run_id':path.name,'status':'invalid','source':path.relative_to(ROOT).as_posix(),'reason':'Malformed or interrupted run metadata','profile':'unknown','filter':'unknown','operation':'unknown'}
    profile=cfg.get('profile','vendor-hid');operation=cfg.get('operation','forward');filter_name=cfg.get('filter','baseline')
    result={'run_id':cfg['run_id'],'requested_hz':cfg['requested_hz'],'samples_requested':cfg['samples'],'status':'invalid','source':str(path.relative_to(ROOT)).replace('\\','/'),'version':cfg['version'],'utc':cfg['utc'],'profile':profile,'filter':filter_name,'operation':operation,'executable_hashes_recorded':bool(cfg.get('build_identity'))}
    result['purpose']=cfg.get('purpose','latency')
    try:
        if (path/'invalidated.json').exists():raise AssertionError(json.loads((path/'invalidated.json').read_text())['reason'])
        assert json.loads((path/'orchestration.json').read_text(encoding='utf-8-sig'))['status']=='completed','Orchestration did not complete'
        assert not list(path.glob('*-error.json')),'Native error record'
        sent=rows(path/'submission.csv');received=rows(path/'reception.csv');warm=cfg['warmup'];freq=cfg['qpc_frequency'];assert freq>0
        assert len(sent)==cfg['samples']+warm,'Submission row count mismatch'
        assert [r['sequence'] for r in sent]==list(range(len(sent))),'Submission sequence mismatch'
        assert all(r['return_qpc']>=r['submit_qpc'] for r in sent),'Invalid submission clock order'
        expected={r['sequence']:r for r in sent}
        if profile!='vendor-hid':
            if profile=='keyboard':assert len(received)==len(sent),'Keyboard sequence correlation requires complete stream'
            if filter_name!='baseline':
                adapter=json.loads((path/'adapter-done.json').read_text())
                assert adapter['captured']==len(sent),'Filter did not capture the complete generated stream'
                stack=(path/'pnp-stack.txt').read_text(encoding='utf-8-sig')
                assert ('InterceptorKeyboardMouse' if filter_name=='Keyboard-Mouse' else 'Interceptor') in stack,'Filter attachment not evidenced in PnP stack'
                if operation=='modify':assert adapter['modified']==len(sent),'Modification not demonstrated'
                if operation=='block':
                    assert adapter['blocked']==sum((r['sequence']+1)%2 for r in sent),'Blocking not demonstrated'
                    assert all((r['sequence']+1)%2==0 for r in received),'Blocked input reached independent receiver'
            received=[dict(r,submit_qpc=expected[r['sequence']]['submit_qpc']) for r in received if r['sequence'] in expected]
        assert all(r['sequence'] in expected and r['submit_qpc']==expected[r['sequence']]['submit_qpc'] and r['receive_qpc']>=r['submit_qpc'] and r['content_valid']==1 for r in received),'Invalid contents, sequence or clock correlation'
        measured=[r for r in received if r['sequence']>=warm]
        ids=[r['sequence'] for r in measured];unique=set(ids)
        latency=np.array([(r['receive_qpc']-r['submit_qpc'])*1e6/freq for r in measured])
        assert latency.size>0,'No measured report received'
        assert len(ids)==len(unique),'Duplicated reports invalidate latency series'
        submit=[r for r in sent if r['sequence']>=warm];delta=(submit[-1]['submit_qpc']-submit[0]['submit_qpc'])/freq
        expected_count=sum((r['sequence']+1)%2==0 for r in submit) if operation=='block' else cfg['samples']
        result.update(status='measured',received=len(measured),missing=expected_count-len(unique),duplicates=len(ids)-len(unique),reordered=sum(a>b for a,b in zip(ids,ids[1:])),submission_errors=sum(r['error']!=0 for r in submit),loss_fraction=(expected_count-len(unique))/expected_count,observed_submission_hz=(len(submit)-1)/delta if delta else 0,p50_us=float(np.percentile(latency,50)),p90_us=float(np.percentile(latency,90)),p95_us=float(np.percentile(latency,95)),p99_us=float(np.percentile(latency,99)),mean_us=float(np.mean(latency)),stdev_us=float(np.std(latency,ddof=1)) if len(latency)>1 else 0,min_us=float(np.min(latency)),max_us=float(np.max(latency)),submission_p50_us=float(np.median([(r['return_qpc']-r['submit_qpc'])*1e6/freq for r in submit])),clock_frequency=freq)
        result['hashes']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(path.iterdir()) if p.is_file()}
    except (AssertionError,KeyError,ValueError,FileNotFoundError) as e:result['reason']=str(e)
    return result
def main():
    results=[analyze(p.parent) for p in sorted((ROOT/'data/raw').rglob('run.json'))]
    output=ROOT/'data/processed/results.json';output.write_text(json.dumps(results,indent=2)+'\n',encoding='utf8')
    print('Validated:',sum(r['status']=='measured' for r in results),'measured;',sum(r['status']!='measured' for r in results),'invalid')
    return results
if __name__=='__main__':main()
