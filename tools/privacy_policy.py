from pathlib import Path
import base64,hashlib,re

def write_privacy(site, config):
    for lang in ("en", "pl"):
        write_privacy_language(site, config, lang)

def write_privacy_language(site, config, lang):
    site=Path(site);dist=site/'docs'
    page=(site/('content/privacy-policy-pl.html' if lang=='pl' else 'content/privacy-policy.html')).read_text()
    prefix='../../' if lang=='pl' else '../'
    route='pl/privacy/' if lang=='pl' else 'privacy/'
    match=re.search(r'<style>(.*?)</style>',page,re.S)
    assert match, 'Approved policy stylesheet required'
    css=match[1]
    def font(m):
        raw=base64.b64decode(m[1],validate=True)
        name='privacy-'+hashlib.sha256(raw).hexdigest()[:16]+'.ttf'
        target=dist/'assets/fonts'/name
        if target.exists():assert target.read_bytes()==raw
        else:target.write_bytes(raw)
        return 'url(fonts/'+name+')'
    css=re.sub(r'url\(data:font/ttf;base64,([^)]*)\)',font,css)
    css+='\nhtml[lang=pl] h1{font-size:clamp(48px,9.5vw,110px)}\n.effective-date{font-size:13px;color:var(--muted);margin:0 0 18px}\n'
    (dist/'assets/privacy-policy.css').write_text(css.replace('#ff792f','#ff6900'))
    replacement='<link rel="icon" href="../assets/favicon.png" type="image/png"><link rel="stylesheet" href="../assets/privacy-policy.css?v=campaign-vinyl-v2-20261110">'
    replacement=replacement.replace('../assets/',prefix+'assets/').replace('campaign-vinyl-v2-20261110','news-20261112')
    page=page[:match.start()]+replacement+page[match.end():]
    robots='noindex, nofollow' if config['preview'] else 'index, follow'
    page=page.replace('</head>','<meta name="robots" content="'+robots+'"></head>',1)
    origin=config.get('site_url')
    if origin:
        from html import escape
        page=page.replace('</head>','<link rel="canonical" href="'+escape(origin.rstrip('/')+'/'+route)+'"></head>',1)
    target=dist/route
    target.mkdir(parents=True,exist_ok=True)
    (target/'index.html').write_text(page)
