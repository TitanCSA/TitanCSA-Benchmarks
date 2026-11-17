from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import json,sys
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.canonical=False;self.description=False;self.schemas=[];self.schema=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ['a','img','link','script']:
   value=a.get('href',a.get('src'))
   if value:self.links.append(value)
  if tag=='link' and a.get('rel')=='canonical':self.canonical=True
  if tag=='meta' and a.get('name')=='description':self.description=True
  if tag=='script' and a.get('type')=='application/ld+json':self.schema=True
 def handle_endtag(self,tag):
  if tag=='script':self.schema=False
 def handle_data(self,data):
  if self.schema:self.schemas.append(json.loads(data))
def main():
 errors=[];pages=list((ROOT/'site').rglob('*.html'))
 for p in pages:
  if p.name=='404.html':continue
  parser=Links();parser.feed(p.read_text(encoding='utf8'))
  if not parser.canonical or not parser.description:errors.append(str(p)+' lacks canonical/description')
  for value in parser.links:
   url=urlparse(value)
   if url.scheme or url.netloc or not url.path or url.path.startswith('/'):continue
   target=(p.parent/unquote(url.path)).resolve()
   if not target.exists():errors.append(f'{p.relative_to(ROOT)}: missing {value}')
 assert not errors,'\n'.join(errors)
 assert (ROOT/'site/sitemap.xml').exists()
 assert (ROOT/'site/assets/raw-results.zip').is_file()
 print('Validated',len(pages),'HTML pages: local links, metadata, JSON-LD and downloadable data')
if __name__=='__main__':main()
