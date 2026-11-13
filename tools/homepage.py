"""English and authored Polish landing page. Public artwork only."""
from html import escape
from pathlib import Path
import struct

def image_size(file):
    data=(Path(__file__).resolve().parents[1]/'docs/assets'/file.split('?')[0]).read_bytes()
    if data.startswith(b'\x89PNG'):
        return struct.unpack('>II',data[16:24])
    if data[:2]==b'\xff\xd8':
        i=2
        while i<len(data):
            if data[i]!=255:i+=1;continue
            while data[i]==255:i+=1
            marker=data[i];i+=1
            if marker in [0xd8,0xd9]:continue
            size=int.from_bytes(data[i:i+2],'big')
            if marker in [0xc0,0xc1,0xc2,0xc3]:
                return int.from_bytes(data[i+5:i+7],'big'),int.from_bytes(data[i+3:i+5],'big')
            i+=size
    raise ValueError('Unrecognized artwork dimensions: '+file)

def render_home(language, config):
    pl = language == 'pl'
    def t(en, polish): return polish if pl else en
    def image(file, alt, width, height, cls='', label=None):
        if file.startswith('web/') and '?' not in file:file+='?v=mobile-ux-v2'
        width,height=image_size(file)
        title=escape(label or t('Enlarge: ','Powiększ: ')+alt,quote=True)
        alt=escape(alt,quote=True)
        return f'<figure class="ui-figure {cls}"><button class="image-open" data-image="/assets/{file}" data-alt="{alt}" aria-label="{title}"><img src="/assets/{file}" width="{width}" height="{height}" loading="lazy" decoding="async" alt="{alt}"></button></figure>'
    def section_head(number, label, title, description):
        return f'<div class="feature-heading"><p class="eyebrow">{number} / {label}</p><h2>{title}</h2><p class="section-description">{description}</p></div>'
    def guide(anchor,en,polish):
        return f'<a class="text-link" href="/support/#{anchor}">{t(en,polish)} <span aria-hidden="true">↗</span></a>'
    def pro(): return '<span class="pro-label">PRO</span>'
    title=t('GØ-404 — Make Beats. Anywhere.','GØ-404 — Twoja bitmaszyna. Zawsze pod ręką.')
    description=t('A hands-on sampler, sequencer and performance machine for iPhone and iPad. Chop samples, scratch, shape your sound and make beats anywhere.',
                  'Sampler, sekwencer i bitmaszyna na iPhone’a i iPada. Tnij sample, scratchuj, kształtuj brzmienie i twórz bity, gdzie chcesz.')
    store=config.get('app_store_url')
    badge='<img src="/assets/download-on-the-app-store.svg" width="120" height="40" alt="Download on the App Store">'
    store_link=(f'<a class="app-store-badge" href="{escape(store)}">{badge}</a>'if store else
                f'<button class="app-store-badge" disabled aria-label="{t("App Store release coming soon","Premiera w App Store już wkrótce")}">{badge}</button><p class="app-store-status">{t("Coming soon to the App Store.","Premiera w App Store już wkrótce.")}</p>')
    phone_alt=t('GØ-404 on iPhone: the complete machine, four illuminated pads, original controls and sequencer.',
                'GØ-404 na iPhonie: cała maszyna, cztery podświetlone pady, oryginalne kontrolki i sekwencer.')
    ipad_alt=t('GØ-404 on iPad, keeping the original narrow machine with black side margins.',
               'GØ-404 na iPadzie, z zachowanymi proporcjami maszyny i czarnymi bokami.')
    body=f'''<main id="main">
<section class="hero" aria-labelledby="hero-title">
  <div class="hero-copy"><p class="eyebrow">SAMPLER. SEQUENCER. PERFORMANCE.</p>
    <h1 id="hero-title">MAKE BEATS.<br><span>ANYWHERE.</span></h1>
    <p class="hero-subtitle">{t('YOUR POCKET BEAT MACHINE.','TWOJA BITMASZYNA.<br>ZAWSZE POD RĘKĄ.')}</p>
    <p class="hero-description">{t('Find a sound. Chop it. Build your groove. A hands-on instrument for iPhone and iPad.','Znajdź dźwięk. Potnij go. Zbuduj groove. Instrument na iPhone’a i iPada, który masz zawsze przy sobie.')}</p>
    <a class="button button-orange hero-cta" href="#inside">{t('SEE THE MACHINE','ZOBACZ MASZYNĘ')} <span aria-hidden="true">↓</span></a>
  </div>
  <figure class="hero-product" id="devices"><div class="device-phone"><img src="/assets/machine-phone-mobile.svg?v=ux-v1" width="1350" height="2760" fetchpriority="high" decoding="async" alt="{phone_alt}"></div></figure>
  <div class="hero-store">{store_link}</div>
</section>
<div class="spec-strip" aria-label="{t('At a glance','W skrócie')}"><span>SAMPLE &amp; CHOP</span><span>16 / 32 STEPS</span><span>PERFORM &amp; RESAMPLE</span><span>WAV EXPORT</span></div>

<section class="section machine-section" id="inside" aria-labelledby="machine-title">
  <div class="feature-heading"><p class="eyebrow">01 / {t('SEE THE MACHINE','POZNAJ MASZYNĘ')}</p><h2 id="machine-title">{t('HANDS ON.<br><span class="orange">HEAD NOD.</span>','RĘCE NA PADACH.<br><span class="orange">GŁOWA W RYTMIE.</span>')}</h2><p class="section-description">{t('Pads, knobs, swing and a sequencer. A hardware-inspired workflow, wherever the beat finds you.','Pady, gałki, swing i sekwencer. Praca jak na sprzętowej bitmaszynie — tam, gdzie złapie Cię pomysł.')}</p></div>
  <div class="machine-overview"><figure class="ipad-stage"><div class="device-ipad"><img src="/assets/machine-ipad-web.svg?v=ux-v1" width="2300" height="3000" loading="lazy" decoding="async" alt="{ipad_alt}"></div><figcaption><strong>{t('ALSO ON iPAD.','DZIAŁA TAKŻE NA iPADZIE.')}</strong><span>{t('The same GØ-404. Original proportions. More room to play.','Ta sama GØ-404. Oryginalne proporcje maszyny. Więcej miejsca do grania.')}</span></figcaption></figure>
  <div class="machine-notes"><h3>{t('Build the groove.<br>Play the details.','Zbuduj groove.<br>Dopracuj szczegóły.')}</h3><p>{t('Four patterns, Song Mode and 16 / 32-step sequencing. Add swing, then double-tap a step to soften an individual hit.','Cztery patterny, tryb Song i sekwencer 16 / 32 kroki. Dodaj swing. Stuknij krok dwa razy, żeby ściszyć pojedyncze uderzenie.')}</p>
  {image('sequencer.jpg',t('GØ-404 step sequencer with orange steps, pattern controls and mixer.','Sekwencer GØ-404 z pomarańczowymi krokami, patternami i mikserem.'),936,460,'sequencer-detail')}
  {guide('sequencing','Patterns, steps & gestures','Patterny, kroki i gesty (EN)')}</div></div>
</section>

<section class="section sampling-section" id="sampling" aria-labelledby="sampling-title">
  <div class="feature-heading"><p class="eyebrow">02 / SAMPLER · GØ GRAB · CRATE</p><h2 id="sampling-title">SAMPLE FROM<br><span class="orange">OTHER APPS.</span></h2><p class="section-description">{t('Capture an idea with GØ GRAB. Keep it in CRATE. Cut it into your next beat.','Przechwyć pomysł w GØ GRAB. Zachowaj go w CRATE. Potnij i wykorzystaj w kolejnym bicie.')}</p></div>
  <div class="sampling-workflow"><div class="workflow-view"><div class="tabs" role="tablist" aria-label="{t('Explore the workflow','Poznaj sposób pracy')}"><button role="tab" id="tab-sampling" aria-selected="true" aria-controls="panel-sampling">SAMPLING</button><button role="tab" id="tab-sequencing" aria-selected="false" aria-controls="panel-sequencing" tabindex="-1">SEQUENCING</button></div>
    <div role="tabpanel" id="panel-sampling" aria-labelledby="tab-sampling" tabindex="0">{image('web/sampler-real-flutter.jpg',t('Real SLICE panel: waveform, trim markers, Preview, Auto Chop and Pad Assign.','Prawdziwy panel SLICE: waveform, znaczniki cięcia, Preview, Auto Chop i Pad Assign.'),1126,700,'sampler-detail')}<p class="image-caption">CAPTURE · CHOP · CREATE</p></div>
    <div role="tabpanel" id="panel-sequencing" aria-labelledby="tab-sequencing" tabindex="0" hidden>{image('sequencer.jpg',t('Actual step-sequencer controls in GØ-404.','Oryginalne kontrolki sekwencera GØ-404.'),936,460)}<p class="image-caption">16 / 32 STEPS · PATTERN / SONG</p></div>
  </div><p class="workflow-note">{t('Import WAV or record with the microphone. Trim, fade, pitch and Auto Chop, then assign the slices to your pads.','Importuj WAV albo nagraj dźwięk mikrofonem. Przytnij, ustaw fade, zmień pitch, użyj Auto Chop i przypisz fragmenty do padów.')}</p></div>
  <div class="capture-panels"><article><div class="panel-heading"><h3>GØ GRAB</h3>{pro()}</div>{image('web/grab-30s-real-flutter.jpg',t('GØ GRAB capture panel with SAVE LAST 30s.','Panel GØ GRAB z przyciskiem SAVE LAST 30s.'),1122,696)}<p>{t('Keep up to the last 30 seconds made available by iOS. On older and newer iPhones, the app chooses a compatible capture method.','Zachowaj do 30 ostatnich sekund udostępnionych przez iOS. Aplikacja sama wybiera zgodną metodę przechwytywania — na starszych i nowszych iPhone’ach.')}</p></article>
  <article><div class="panel-heading"><h3>CRATE</h3>{pro()}</div>{image('web/crate-real-iphone.jpg',t('CRATE library detail: search, source filters and saved recordings.','Fragment biblioteki CRATE: wyszukiwanie, filtry źródeł i zapisane nagrania.'),1124,982)}<p>{t('One library for captures, USB takes and scratches. Search, preview and trim. Load into SAMPLER to chop, or into a TURNTABLE slot.','Jedna biblioteka nagrań GØ GRAB, USB i scratchy. Szukaj, odsłuchuj i przycinaj. Wczytaj do SAMPLER, żeby pociąć dźwięk, albo do slotu TURNTABLE.')}</p></article></div>
  <p class="small-print">{t('GØ GRAB and CRATE require PRO. Capture only audio you own or have permission to use. Protected content and source apps may restrict recording.','GØ GRAB i CRATE wymagają PRO. Nagrywaj materiały, do których masz prawa lub zgodę. Aplikacje źródłowe i zabezpieczone treści mogą ograniczać przechwytywanie.')}</p>{guide('sampling','Sampling & capture guide','Sampling i przechwytywanie (EN)')}
</section>

<section class="section performance" id="performance" aria-labelledby="fx-title">
  <div class="feature-heading"><p class="eyebrow">03 / TONE FX + PERFORMANCE FX</p><h2 id="fx-title">SHAPE YOUR<br><span class="orange">SOUND.</span></h2><p class="section-description">{t('Texture in the sound. Movement in the performance. Put your hands on both.','Nadaj brzmieniu charakter. Dodaj ruch podczas grania. Wszystko pod palcami.')}</p></div>
  <div class="sound-fx-grid"><article><h3>TONE FX</h3>{image('web/campaign-tone-fx.jpg',t('Actual TONE FX: Vinyl Glue, Cassette, Vinyl Noise, Drive, Lo-Fi, Dirt Glitch and Pitch Mod.','TONE FX: Vinyl Glue, Cassette, Vinyl Noise, Drive, Lo-Fi, Dirt Glitch i Pitch Mod.'),1000,530)}<p>{t('Vinyl warmth, cassette colour, saturation and grit. Shape the character of the machine.','Ciepło winylu, kolor kasety, nasycenie i brud. Zbuduj własny charakter maszyny.')}</p><ul class="effect-list"><li>VINYL GLUE</li><li>CASSETTE</li><li>VINYL NOISE</li><li>DRIVE</li><li>LO-FI</li><li>DIRT GLITCH</li><li>PITCH MOD</li></ul></article>
  <article><h3>PERFORMANCE FX</h3>{image('web/campaign-performance-fx.jpg',t('Actual PERFORMANCE FX: Super Filter, Isolator, Tape Echo, Pitch All, Looper, Vinyl Stop and Mute Drums.','PERFORMANCE FX: Super Filter, Isolator, Tape Echo, Pitch All, Looper, Vinyl Stop i Mute Drums.'),1000,530)}<p>{t('Filter, echo and loop the beat live. Combine LOOPER with MUTE DRUMS. HOLD keeps the effect engaged.','Filtruj, zapętlaj i dodawaj echo na żywo. Łącz LOOPER z MUTE DRUMS. HOLD utrzyma efekt, gdy ręce zajmą się czymś innym.')}</p><ul class="effect-list"><li>SUPER FILTER</li><li>ISOLATOR</li><li>TAPE ECHO</li><li>PITCH ALL</li><li>LOOPER</li><li>MUTE DRUMS</li><li>VINYL STOP</li></ul></article></div>
  {guide('performance','Performance FX guide','PERFORMANCE FX w praktyce (EN)')}
</section>

<section class="section turntable-section" id="turntable" aria-labelledby="turntable-title"><span id="capture" class="anchor-alias"></span>
  <div class="turntable-layout"><div class="feature-heading"><p class="eyebrow">04 / GØ TURNTABLE</p><h2 id="turntable-title">CUT.<br>SCRATCH.<br><span class="orange">REPEAT.</span></h2><p class="section-description">{t('Load your own sound. Work the platter and crossfader over your beat.','Załaduj własny dźwięk. Tnij crossfaderem i scratchuj do swojego bitu.')}</p><p class="turntable-motto">FREE TO SCRATCH.<br>PRO TO GO FURTHER.</p><dl class="slot-access"><div><dt>FREE</dt><dd>{t('2 scratch slots','2 sloty do scratchowania')}</dd></div><div><dt>PRO</dt><dd>{t('4 slots + performance recording','4 sloty + nagrywanie występu')}</dd></div></dl>{guide('turntable','Explore TURNTABLE','Poznaj TURNTABLE (EN)')}</div>
  {image('web/campaign-turntable.jpg',t('Actual GØ TURNTABLE with platter, sample slots, crossfader, mixer and recording controls.','Oryginalny GØ TURNTABLE: talerz, sloty sampli, crossfader, mikser i kontrolki nagrywania.'),1206,2622,'turntable-detail')}</div>
</section>

<section class="section bass-section" id="instruments" aria-labelledby="bass-title">
  <div class="feature-heading"><p class="eyebrow">05 / BANK B · BASS &amp; INSTRUMENT</p><h2 id="bass-title">BRING THE<br><span class="orange">LOW END.</span></h2><p class="section-description">{t('Build a bassline. Find a melody. Make the whole beat yours.','Zbuduj linię basu. Znajdź melodię. Nadaj bitowi własny styl.')}</p></div>
  <div class="bass-layout">{image('web/bass-real-flutter.jpg',t('Actual bank B BASS editor: Analog Bass, Tone, Length, Level, Octave and Randomize.','Prawdziwy edytor BASS banku B: Analog Bass, Tone, Length, Level, Octave i Randomize.'),1126,1244,'bass-detail')}
  <div class="bass-copy"><h3>{t('A bass voice.<br>A melodic voice.','Bas.<br>I miejsce na melodię.')}</h3><p>{t('B1–B8 for bass. B9–B16 for instruments. Choose a sound, shape it in SOUND and FX, then play notes into the beat.','B1–B8 to bas, B9–B16 to instrumenty. Wybierz brzmienie, dopracuj je w SOUND i FX, a potem dograj nuty do bitu.')}</p><div class="inline-feature"><p class="eyebrow">AUTO KEY</p><p>{t('Analyze samples on A9–A16 and tune the bass and instruments to match.','Przeanalizuj sample z A9–A16 i dopasuj do nich strój basu oraz instrumentów.')}</p></div>{guide('bank-b','Bass, instruments & Auto Key','Bas, instrumenty i Auto Key (EN)')}</div></div>
</section>

<section class="section vintage-section" id="vintage" aria-labelledby="vintage-title">
  <div class="feature-heading"><p class="eyebrow">06 / VINTAGE · RESAMPLING</p><h2 id="vintage-title">OLD SCHOOL.<br><span class="orange">NEW RULES.</span></h2><p class="section-description">{t('Three sampling characters. Your original source stays yours.','Trzy charaktery samplingu. Oryginalny materiał pozostaje nienaruszony.')}</p></div>
  <div class="vintage-layout">{image('pad-edit-vintage-model-lamps-20261110.png?v=stereo-compact-v3',t('Actual PAD EDIT with waveform, Stereo control, Vintage and the 1200, 60 and 3000 models.','Prawdziwy PAD EDIT: waveform, Stereo, Vintage i modele 1200, 60 oraz 3000.'),780,1688,'vintage-detail')}
  <div class="vintage-controls"><div class="model-bank" role="tablist" aria-label="{t('Vintage sampling character','Charakter samplingu Vintage')}">'''
    models=[('1200',t('RAW TEXTURE','SUROWA FAKTURA'),t('A little rough around the edges.','Odrobina surowości.'),t('Grainier digital texture for drum hits and chopped phrases.','Ziarnista, cyfrowa faktura dla perkusji i pociętych fraz.')),
            ('60',t('WARM CHARACTER','CIEPŁY CHARAKTER'),t('Warmth with a different weight.','Ciepło, które ma swój ciężar.'),t('A different feel for a bass phrase, chord or drum hit.','Inny charakter linii basu, akordu czy uderzenia perkusji.')),
            ('3000',t('FOCUSED DETAIL','WYRAŹNY DETAL'),t('Texture with room for detail.','Faktura z miejscem na detal.'),t('A focused finish that keeps the identity of your source.','Wyraziste wykończenie z zachowaniem charakteru źródła.'))]
    for i,(model,tag,_,_) in enumerate(models):
        body+=f'<button class="model-key" role="tab" id="model-{model}" aria-controls="character-{model}" aria-selected="{"true"if not i else"false"}" tabindex="{0 if not i else -1}"><span class="model-led" aria-hidden="true"></span><span class="model-number">{model}</span><span class="model-tag">{tag}</span></button>'
    body+='</div><div class="character-info">'
    for i,(model,tag,heading,description_) in enumerate(models):
        body+=f'<div role="tabpanel" id="character-{model}" aria-labelledby="model-{model}" tabindex="0" {"hidden"if i else""}><h3>{heading}</h3><p>{description_}</p></div>'
    body+=f'''<p class="small-print">{t('Choose THIS PAD or the current group of eight. Vintage-inspired characters, not claims of identical hardware emulation.','Wybierz THIS PAD lub bieżącą grupę ośmiu padów. Modele inspirowane klasycznym sprzętem, bez deklarowania identycznej emulacji.')}</p></div>{guide('vintage-help','Normalize & Vintage guide','Normalize i Vintage (EN)')}</div></div>
  <div class="resample-story"><div><p class="eyebrow">FLIP IT. RESAMPLE IT.</p><h3>{t('The performance<br>becomes the sample.','Z występu<br>powstaje nowy sampel.')}</h3><p>{t('Print a pattern, song or live pass with performance FX. In PAD EDIT → RESAMPLE, send one processed sound to another pad and keep the source.','Zapisz pattern, song lub występ z PERFORMANCE FX jako nowy dźwięk. W PAD EDIT → RESAMPLE przenieś przetworzony dźwięk na inny pad, zachowując źródło.')}</p>{guide('pad-resample','Two ways to resample','Dwa sposoby resamplingu (EN)')}</div>{image('resample-waveform.jpg',t('Waveform selection in PAD RESAMPLE.','Wybór fragmentu waveformu w PAD RESAMPLE.'),900,322)}</div>
  <div class="edit-features"><article><h3>TIME STRETCH</h3><p>{t('Change length, keep the pitch. Drag the waveform handle or use FIT TO BPM. THIS PAD / ALL works within the current group of eight.','Zmień długość bez zmiany wysokości dźwięku. Przeciągnij uchwyt waveformu lub użyj FIT TO BPM. THIS PAD / ALL działa w bieżącej grupie ośmiu padów.')}</p>{guide('time-stretch','Stretch & Fit to BPM','Stretch i Fit to BPM (EN)')}</article><article><h3>SIDECHAIN</h3><p>{t('Let a chosen bank A pad make room in your samples, bass or instruments. Set amount and release, for one pad or the group.','Wybrany pad banku A robi miejsce w samplach, basie lub instrumentach. Ustaw Amount i Release dla jednego pada lub całej grupy.')}</p>{guide('sidechain','Sidechain guide','Jak używać SIDECHAIN (EN)')}</article></div>
</section>

<section class="section ownership" id="free-pro" aria-labelledby="ownership-title"><div class="feature-heading"><p class="eyebrow">07 / FREE &amp; PRO</p><h2 id="ownership-title">YOUR BEAT.<br><span class="orange">YOUR MACHINE.</span></h2><p class="section-description">{t('The core instrument stays free. PRO adds capture, a sample library and more ways to take your music further.','Podstawowa bitmaszyna jest darmowa. PRO dodaje przechwytywanie, bibliotekę sampli i więcej możliwości pracy z muzyką.')}</p></div><div class="comparison">'''
    free=[t('Unlimited local projects','Nieograniczone projekty lokalne'),t('Sampling, Auto Chop & per-pad editing','Sampling, Auto Chop i edycja padów'),t('16 / 32 steps, swing & Song Mode','16 / 32 kroki, swing i tryb Song'),t('Core FX, Vintage & resampling','Podstawowe FX, Vintage i resampling'),t('TURNTABLE: 2 scratch slots','TURNTABLE: 2 sloty do scratchowania'),t('Time Stretch, Sidechain & MIDI Learn','Time Stretch, Sidechain i MIDI Learn'),t('Bass & instrument voices','Bas i instrumenty'),t('WAV export','Eksport WAV'),t('Included drum kits & free faceplates','Fabryczne zestawy perkusji i darmowe faceplate’y')]
    premium=['GØ GRAB',t('CRATE & USB SAMPLING','CRATE i USB SAMPLING'),t('TURNTABLE: 4 slots + performance recording','TURNTABLE: 4 sloty + nagrywanie występu'),t('STEMS export','Eksport STEMS'),t('GØ BACKUP to your private iCloud','GØ BACKUP do prywatnego iCloud'),t('GØ TAPES drum pack','Pakiet perkusyjny GØ TAPES'),t('ANALOG ROOTS faceplate pack','Pakiet faceplate’ów ANALOG ROOTS')]
    for name,items,label in [('FREE',free,t('THE CORE INSTRUMENT','PODSTAWOWA MASZYNA')),('PRO',premium,t('GO FURTHER','WIĘCEJ MOŻLIWOŚCI'))]:
        body+=f'<article><div class="tier-heading"><h3>{name}</h3><span>{label}</span></div><ul>'+''.join(f'<li>{item}</li>'for item in items)+'</ul></article>'
    body+=f'''</div><p class="small-print">{t('PRO is a subscription. Plans and localized prices are shown by Apple in the app. Drum and faceplate packs sold separately remain separate purchases.','PRO jest subskrypcją. Plany i lokalne ceny pokazuje Apple w aplikacji. Pakiety perkusji i faceplate’ów sprzedawane osobno są niezależnymi zakupami.')}</p>
<div class="make-yours"><div><p class="eyebrow">MAKE IT YOURS.</p><h3>{t('Your sound.<br>Your front panel.','Twoje brzmienie.<br>Twoja obudowa.')}</h3><p>{t('Start with GØ DUST. Add GØ STREETS, GØ CRATES or your own samples. Pick a faceplate that feels like your machine.','Zacznij od GØ DUST. Sięgnij po GØ STREETS, GØ CRATES lub własne sample. Wybierz faceplate, który pasuje do Twojej maszyny.')}</p><p class="small-print">{t('Store availability will be confirmed at release.','Dostępność pakietów w sklepie zostanie potwierdzona na premierę.')}</p></div><div class="faceplate-gallery" aria-label="{t('Three real faceplate designs','Trzy prawdziwe wersje wyglądu')}">'''
    for name,file,label in [('ORANGE DUST','orange-dust',t('FREE DESIGN','DARMOWY WZÓR')),('RAW METAL','raw-metal',t('FREE DESIGN','DARMOWY WZÓR')),('SOUL CONSOLE','soul-console',t('PRO DESIGN','WZÓR PRO'))]:
        body+=f'<div>{image("faceplate-machine-"+file+".png",t("Actual GØ-404 with the ","Prawdziwa GØ-404 z faceplate’em ")+name,780,1688)}<p class="image-caption">{name}<span>{label}</span></p></div>'
    body+=f'''</div></div></section>

<section class="section connections" id="connections" aria-labelledby="connections-title"><div class="feature-heading"><p class="eyebrow">08 / {t('CONNECT. SAVE. KEEP CREATING.','PODŁĄCZ. ZAPISZ. TWÓRZ DALEJ.')}</p><h2 id="connections-title">{t('BEYOND<br><span class="orange">THE PADS.</span>','WIĘCEJ<br><span class="orange">NIŻ PADY.</span>')}</h2></div><div class="tool-list">'''
    tools=[('USB SAMPLING',True,'usb',t('Record compatible external audio by USB‑C or a Lightning USB host adapter. Check the input, REC, then STOP → CRATE. USB audio compatibility varies; it is separate from MIDI.','Nagrywaj ze zgodnego wejścia audio przez USB‑C lub adapter USB host do Lightning. Sprawdź wejście, naciśnij REC, potem STOP → CRATE. Zgodność zależy od sprzętu; USB audio i MIDI to osobne funkcje.')),
           ('MIDI LEARN',False,'midi',t('Connect a controller by USB‑C or Lightning USB host adapter. Map supported pads, buttons and knobs, and keep the setup for your next session.','Podłącz kontroler przez USB‑C lub adapter USB host do Lightning. Przypisz obsługiwane pady, przyciski i gałki. Mapowanie zostanie na następną sesję.')),
           ('WAV / STEMS',False,'export',t('Export a pattern, song or RES as WAV. PRO adds separate stems for mixing.','Eksportuj pattern, song lub RES do WAV. PRO dodaje osobne ślady do miksowania.')),
           ('GØ BACKUP',True,'backup',t('Back up saved projects, CRATE and the four-slot TURNTABLE bank to your private iCloud. Keep your work ready for the next session.','Zabezpiecz zapisane projekty, CRATE i cztery sloty TURNTABLE w swoim prywatnym iCloud. Zachowaj materiał na kolejną sesję.')),
           (t('PROJECTS & FOLDERS','PROJEKTY I FOLDERY'),False,'projects',t('Save, overwrite or create a new copy. Organize projects into your own folders when you need them.','Zapisz projekt, nadpisz go lub utwórz nową kopię. Organizuj bity we własnych folderach, jeśli tego potrzebujesz.'))]
    for name,premium_,anchor,copy in tools:
        body+=f'<article><div class="tool-name"><h3>{name}</h3>{pro()if premium_ else""}</div><div><p>{copy}</p>{guide(anchor,"Explore the workflow","Zobacz, jak to działa (EN)")}</div></article>'
    body+=f'''</div><div class="closing-line"><p>YOUR NEXT BEAT<br><span class="orange">STARTS HERE.</span></p><a class="button button-light" href="/support/">{t('GET TO KNOW GØ-404','POZNAJ GØ-404 (EN)')} ↗</a></div></section>
</main>'''
    newsletter_url=config.get('newsletter_form_url')
    if newsletter_url:
        from urllib.parse import urlsplit
        parsed=urlsplit(newsletter_url)
        assert parsed.scheme=='https' and parsed.netloc=='ab7bda5a.sibforms.com' and parsed.path.startswith('/v2/serve/') and '\\' not in newsletter_url
        newsletter=f'<section class="section newsletter-section" id="news" aria-label="GØ-404 NEWS"><iframe class="newsletter-frame" title="{t("GØ-404 NEWS sign-up form — Brevo","Formularz zapisu GØ-404 NEWS — Brevo")}" width="1100" height="220" src="/newsletter/?v=final-strip-v5-20261112" data-newsletter-frame loading="lazy" referrerpolicy="strict-origin-when-cross-origin" scrolling="auto"></iframe><p class="newsletter-note">{t("Confirm your email to join. Leave anytime.","Potwierdź e-mail, aby dołączyć. Możesz zrezygnować w każdej chwili.")} <a href="{t("/privacy/","/pl/privacy/")}">{t("Privacy Policy","Polityka prywatności")}</a>.</p></section>'
        body=body.replace('<div class="spec-strip"',newsletter+'\n<div class="spec-strip"',1)
    return body,title,description
