"""Local-only visual verification; uses an existing Chrome installation."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'.local/previews';out.mkdir(parents=True,exist_ok=True)
errors=[];checked=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
    for width in [1440,390]:
        page=browser.new_page(viewport={'width':width,'height':960 if width==1440 else 844},device_scale_factor=1,color_scheme='light')
        page.on('pageerror',lambda e:errors.append(str(e)))
        for route in ['', 'vdevice/latency/','vdevice/comparisons/','vdevice/joystick/','interceptor/results/','gamepad/results/','methodology/incident-wdf-001/','data/']:
            response=page.goto('http://127.0.0.1:8768/'+route,wait_until='networkidle')
            assert response.status==200,(route,response.status)
            assert page.locator('h1').count()==1,route
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'),(route,width,'body overflow')
            checked.append({'route':route,'width':width,'status':response.status,'title':page.title()})
        page.goto('http://127.0.0.1:8768/',wait_until='networkidle')
        page.screenshot(path=str(out/f'home-{width}.png'),full_page=True)
        assert page.get_by_text('Open stability incident',exact=True).count()>0
        if width==1440:
            page.locator('label[for="__palette_1"]').click()
            assert page.locator('body').get_attribute('data-md-color-scheme')=='slate'
            page.screenshot(path=str(out/'home-dark.png'),full_page=True)
        page.close()
    browser.close()
assert not errors,errors
(out/'browser-qa.json').write_text(json.dumps({'checked':checked,'page_errors':errors},indent=2)+'\n')
print('Browser verified desktop/mobile:',len(checked),'page views; no overflow or page errors')
