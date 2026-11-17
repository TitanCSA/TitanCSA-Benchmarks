"""GitHub REST helper. Credentials remain in memory; never log headers."""
import json,os,subprocess,urllib.request,urllib.error
class API:
    def __init__(self,authenticate=False):
        self.headers={'Accept':'application/vnd.github+json','User-Agent':'TitanCSA-Benchmarks','X-GitHub-Api-Version':'2022-11-28'}
        if authenticate:
            p=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\nusername=TitanCSA\n\n',text=True,capture_output=True,check=True,env=dict(os.environ,GIT_TERMINAL_PROMPT='0',GCM_INTERACTIVE='Never'))
            fields=dict(x.split('=',1) for x in p.stdout.splitlines() if '=' in x)
            self.headers['Authorization']='Bearer '+fields['password']
            assert self.call('GET','/user')['login'].lower()=='titancsa'
    def call(self,method,path,data=None):
        assert path.startswith('/') and not path.startswith('//')
        payload=None if data is None else json.dumps(data).encode()
        req=urllib.request.Request('https://api.github.com'+path,data=payload,headers=dict(self.headers,**({'Content-Type':'application/json'} if data is not None else {})),method=method)
        try:
            with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)
        except urllib.error.HTTPError as e:
            raise RuntimeError(f'GitHub {method} {path}: HTTP {e.code}') from None
