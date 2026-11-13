"""Static release checks. No browser, network, installation or deployment."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib, json, re, subprocess
from homepage import image_size

SITE=Path(__file__).resolve().parents[1]
DOCS=SITE/'docs'
errors=[]
checks=[]
class Page(HTMLParser):
    def __init__(self, file):
        super().__init__(); self.file=file; self.ids=set();self.links=[];self.images=[];self.lang=None;self.alternates=[];self.canonical=None;self.h1=0;self.languageLinks={}
        self.feed(file.read_text())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id'in a:
            if a['id']in self.ids:errors.append(str(self.file)+': duplicate id '+a['id'])
            self.ids.add(a['id'])
        if tag=='html':self.lang=a.get('lang')
        if tag=='a'and a.get('data-language'):self.languageLinks[a['data-language']]=a.get('href')
        if tag=='h1':self.h1+=1
        if tag=='link'and a.get('rel')=='canonical':self.canonical=a.get('href')
        if tag=='link'and a.get('rel')=='alternate':self.alternates.append(a)
        if tag=='img':self.images.append(a)
        for key in ['href','src','data-image']:
            if a.get(key):self.links.append(a[key])

pages={p:Page(p)for p in DOCS.rglob('*.html')}
for file,page in pages.items():
    expected_h1=0 if file==DOCS/'newsletter/index.html' else 1
    if page.h1!=expected_h1:errors.append(f'{file}: expected {expected_h1} h1, got {page.h1}')
    for link in page.links:
        url=urlsplit(link)
        if url.scheme or url.netloc or not url.path and not url.fragment:continue
        target=DOCS/unquote(url.path.lstrip('/')) if url.path.startswith('/') else file.parent/unquote(url.path)
        if not url.path:target=file
        if target.is_dir():target/='index.html'
        if not target.is_file():errors.append(f'{file.relative_to(DOCS)}: missing {link}');continue
        if url.fragment and target in pages and url.fragment not in pages[target].ids:
            errors.append(f'{file.relative_to(DOCS)}: missing anchor {link}')
    for img in page.images:
        src=img.get('src','')
        if not src:continue # Dialog image is assigned only when opened.
        if not img.get('alt'):errors.append(f'{file}: image without descriptive alt {src}')
        if src.startswith('/assets/') and src.split('?')[0].endswith(('.png','.jpg')):
            actual=image_size(src.removeprefix('/assets/'))
            declared=tuple(int(img.get(n,0))for n in ['width','height'])
            if all(declared) and abs(actual[0]/actual[1]-declared[0]/declared[1])>.005:
                errors.append(f'{file}: image ratio mismatch {src}: {actual} vs {declared}')
    checks.append({'page':'/'+str(file.relative_to(DOCS)),'language':page.lang,'links':len(page.links),'images':len(page.images),'h1':page.h1})
for route,lang in [('index.html','en'),('pl/index.html','pl')]:
    page=pages[DOCS/route]
    assert page.lang==lang
    assert page.languageLinks=={'en':'/','pl':'/pl/'}, 'Language links must open from the top'
    assert {x['hreflang']for x in page.alternates}=={'en','pl','x-default'}
    assert page.canonical=='https://go404.app/'+('pl/'if lang=='pl'else'')
    text=(DOCS/route).read_text()
    assert 'translate="no"'not in text and 'notranslate'not in text
    assert 'loading="lazy"'not in re.search(r'<img src="/assets/machine-phone-mobile.*?>',text)[0]
    assert 'fetchpriority="high"'in text

# Brand names visible to visitors use the same Ø spelling as the instrument.
for file in pages:
    assert not re.search(r'\bGO (?:GRAB|BACKUP|EXPORT|DRUMS|TAPES|FACEPLATES|TURNTABLE)\b',file.read_text()),f'Unbranded feature name: {file}'

# The owner-approved newsletter policy update has an explicit content fingerprint.
# Future substantive policy edits require owner approval and a new fingerprint.
approved=json.loads((SITE/'content/privacy-approved.json').read_text())['sha256']
for file,digest in approved.items():
    assert hashlib.sha256((SITE/file).read_bytes()).hexdigest()==digest,f'Unapproved policy edit: {file}'
assert subprocess.check_output(['git','show','HEAD:docs/CNAME'],cwd=SITE)==(DOCS/'CNAME').read_bytes()
form=(DOCS/'newsletter/index.html').read_text()
assert form==(SITE/'content/newsletter-form.html').read_text()
assert 'email_address_check' in form and 'Check your inbox!' in form
assert 'New features, sounds &amp; releases.<br>Straight to your inbox.' in form
assert 'placeholder="Email address"' in form and 'SIGN ME UP!' in form
assert not re.search(r'Free updates\.|Bezpłatne aktualizacje\.',(DOCS/'index.html').read_text()+(DOCS/'pl/index.html').read_text())
for script in re.findall(r'<script>(.*?)</script>',form,re.S):
    import base64
    digest=base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
    assert "'sha256-"+digest+"'" in form, 'Form inline script blocked by CSP'

for css in (DOCS/'assets').glob('*.css'):
    for link in re.findall(r'url\([\'"]?([^\)\'\"]+)',css.read_text()):
        if link.startswith('data:'):continue
        resource=urlsplit(link).path
        path=DOCS/resource.lstrip('/') if resource.startswith('/') else css.parent/resource
        assert path.exists(),f'Missing CSS resource: {path}'

result={'status':'FAIL'if errors else'PASS','pages':checks,'errors':errors,
        'privacyContentMatchesApprovedHash':True,'newsletterFormVerified':True,'customDomainUnchanged':True,
        'locales':['en','pl'],'brandingCorrect':True,'languageSwitchStartsAtTop':True,'noPublication':True}
out=SITE/'review/ux-20261111';out.mkdir(parents=True,exist_ok=True)
(out/'static-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
