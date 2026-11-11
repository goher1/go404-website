"""Prepare web-sized copies of approved artwork; never change source pixels/UI.

Requires macOS sips only when regenerating. No generation, colour adjustment,
retouching, or new interface elements. Crops are intentional panel details.
"""
from pathlib import Path
import base64, hashlib, json, re, subprocess

SITE = Path(__file__).resolve().parents[1]
ASSETS = SITE / 'docs/assets'
OUTPUT = ASSETS / 'web'
STAGING = SITE / 'review/artwork'
OUTPUT.mkdir(exist_ok=True)
STAGING.mkdir(parents=True, exist_ok=True)
manifest = []

def jpg(source, destination, crop=None, width=None):
    command = ['sips']
    if crop:
        x, y, w, h = crop
        command += ['--cropOffset', str(y), str(x), '--cropToHeightWidth', str(h), str(w)]
    if crop:
        assert width is None or width == crop[2], 'Crop at source size; resize in a separate pass if needed.'
    if width and not crop:
        command += ['--resampleWidth', str(width)]
    command += ['-s', 'format', 'jpeg', '-s', 'formatOptions', '93', str(source), '--out', str(destination)]
    subprocess.run(command, check=True, capture_output=True)
    manifest.append({'source':str(source.relative_to(SITE)), 'output':str(destination.relative_to(SITE)),
                     'sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),
                     'outputSHA256':hashlib.sha256(destination.read_bytes()).hexdigest(),
                     'cropXYWH':crop,'width':width,'bytes':destination.stat().st_size})

for name, crop, width in [
    ('bass-real-flutter',(40,730,1126,1244),1126),
    ('sampler-real-flutter',(40,962,1126,700),1126),
    ('crate-real-iphone',(42,232,1124,982),1124),
    ('grab-30s-real-flutter',(42,1004,1124,700),1124),
]:
    jpg(SITE/'content/artwork'/f'{name}.png', OUTPUT/f'{name}.jpg', crop, width)

for name in ['campaign-tone-fx','campaign-performance-fx']:
    jpg(ASSETS/f'{name}.png', OUTPUT/f'{name}.jpg')
jpg(ASSETS/'campaign-turntable.png', OUTPUT/'campaign-turntable.jpg', (0,184,1206,2340))

# Keep the exact SVG geometry, masks, meter and transparent Apple frame.
# Only the opaque screen layer becomes a high-quality JPEG at its source size.
for name, target in [('machine-phone-lit-v4.svg','machine-phone-mobile.svg'),
                     ('machine-ipad-lit-v4.svg','machine-ipad-web.svg'),
                     ('campaign-ink-grain-v6.svg','campaign-grain-web.svg')]:
    source=ASSETS/name
    svg=source.read_text()
    data=re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)',svg)
    if data:
        opaque=STAGING/(target+'.screen.png')
        opaque.write_bytes(base64.b64decode(data[1]))
        compressed=STAGING/(target+'.screen.jpg')
        jpg(opaque,compressed)
        svg=svg[:data.start()]+'data:image/jpeg;base64,'+base64.b64encode(compressed.read_bytes()).decode()+svg[data.end():]
    (ASSETS/target).write_text(svg)
    manifest.append({'source':str(source.relative_to(SITE)), 'output':'docs/assets/'+target,
                     'sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),
                     'outputSHA256':hashlib.sha256(svg.encode()).hexdigest(), 'bytes':len(svg.encode()),
                     'geometryChanged':False,'meterChanged':False,'frameChanged':False})

(SITE/'content/artwork/provenance.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps([{'output':row['output'],'bytes':row['bytes']}for row in manifest],indent=2))
