"""English and authored Polish landing page. Public artwork only."""
from html import escape
from pathlib import Path
import struct

ART_REVISION = 'ui-20261120'

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
        if file.startswith('web/') and '?' not in file:
            file += f'?v={ART_REVISION}'
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
    phone_alt=t('GØ-404 on iPhone in PATTERN, with 16 pads and steps at different velocities.',
                'GØ-404 na iPhonie w trybie PATTERN, z 16 padami i krokami o różnej głośności.')
    ipad_alt=t('GØ-404 in portrait iPad Fit with the Orange Dust faceplate visible around the machine.',
               'GØ-404 w pionowym trybie iPad Fit z faceplate’em Orange Dust widocznym wokół maszyny.')
    body=f'''<main id="main">
<section class="hero" aria-labelledby="hero-title">
  <div class="hero-copy"><p class="eyebrow">SAMPLER. SEQUENCER. PERFORMANCE.</p>
    <h1 id="hero-title">MAKE BEATS.<br><span>ANYWHERE.</span></h1>
    <p class="hero-subtitle">{t('YOUR POCKET BEAT MACHINE.','TWOJA BITMASZYNA.<br>ZAWSZE POD RĘKĄ.')}</p>
    <p class="hero-description">{t('Find a sound. Chop it. Build your groove. A hands-on instrument for iPhone and iPad.','Znajdź dźwięk. Potnij go. Zbuduj groove. Instrument na iPhone’a i iPada, który masz zawsze przy sobie.')}</p>
    <a class="button button-orange hero-cta" href="#inside">{t('SEE THE MACHINE','ZOBACZ MASZYNĘ')} <span aria-hidden="true">↓</span></a>
  </div>
  <figure class="hero-product" id="devices"><div class="device-phone"><img src="/assets/machine-phone-mobile.svg?v={ART_REVISION}" width="1350" height="2760" fetchpriority="high" decoding="async" alt="{phone_alt}"></div></figure>
  <div class="hero-store">{store_link}</div>
</section>
<div class="spec-strip" aria-label="{t('At a glance','W skrócie')}"><span>SAMPLE &amp; CHOP</span><span>16 / 32 STEPS</span><span>PERFORM &amp; RESAMPLE</span><span>WAV EXPORT</span></div>

<section class="section machine-section" id="inside" aria-labelledby="machine-title">
  <div class="feature-heading"><p class="eyebrow">01 / {t('SEE THE MACHINE','POZNAJ MASZYNĘ')}</p><h2 id="machine-title">{t('HANDS ON.<br><span class="orange">HEAD NOD.</span>','RĘCE NA PADACH.<br><span class="orange">GŁOWA W RYTMIE.</span>')}</h2><p class="section-description">{t('Pads, knobs, swing and a sequencer. A hardware-inspired workflow, wherever the beat finds you.','Pady, gałki, swing i sekwencer. Praca jak na sprzętowej bitmaszynie — tam, gdzie złapie Cię pomysł.')}</p></div>
  <div class="machine-overview"><figure class="ipad-stage"><div class="device-ipad"><img src="/assets/machine-ipad-web.svg?v={ART_REVISION}" width="2300" height="3000" loading="lazy" decoding="async" alt="{ipad_alt}"></div><figcaption><strong>iPAD FIT</strong><span>{t('A portrait layout made for iPad. Switch to CLASSIC in SETTINGS → DISPLAY. Your selected faceplate follows the layout.','Pionowy układ dopasowany do iPada. W SETTINGS → DISPLAY możesz przełączyć się na CLASSIC. Wybrany faceplate dopasuje się do widoku.')}</span></figcaption></figure>
  <div class="machine-notes"><h3>{t('Build the groove.<br>Play the details.','Zbuduj groove.<br>Dopracuj szczegóły.')}</h3><p>{t('Build four patterns with 16 or 32 steps, then arrange them in SONG. Double-tap an active step to cycle its velocity. Add swing and shift each pad up to 100 ms early or late with GROOVE.','Zbuduj cztery patterny po 16 lub 32 kroki i ułóż je w SONG. Stuknij aktywny krok dwa razy, aby zmienić jego głośność. Dodaj swing i przesuń uderzenia wybranego pada do 100 ms wcześniej lub później w GROOVE.')}</p>
  {image('web/sequencer-current.jpg',t('GØ-404 PATTERN sequencer with four step intensities, MIXER and GROOVE.','Sekwencer PATTERN z czterema poziomami głośności kroków, MIXER i GROOVE.'),1152,545,'sequencer-detail')}
  <p>{t('Drag a note’s right edge to set its length on a GATE pad. Tap a track number to select the pad silently, or drag across track numbers to select several for SOLO or MUTE.','Przeciągnij prawą krawędź nuty, aby zmienić jej długość na padzie z GATE. Stuknij numer ścieżki, aby wybrać pad bez dźwięku, albo przeciągnij po numerach, aby zaznaczyć kilka ścieżek do SOLO lub MUTE.')}</p>
  {guide('sequencing','Patterns, steps & gestures','Patterny, kroki i gesty (EN)')}</div></div>
</section>

<section class="section sampling-section" id="sampling" aria-labelledby="sampling-title">
  <div class="feature-heading"><p class="eyebrow">02 / SAMPLER · GØ GRAB · CRATE</p><h2 id="sampling-title">SAMPLE FROM<br><span class="orange">OTHER APPS.</span></h2><p class="section-description">{t('Capture an idea with GØ GRAB. Keep it in CRATE. Cut it into your next beat.','Przechwyć pomysł w GØ GRAB. Zachowaj go w CRATE. Potnij i wykorzystaj w kolejnym bicie.')}</p></div>
  <div class="sampling-workflow"><div class="workflow-view"><div class="tabs" role="tablist" aria-label="{t('Explore the workflow','Poznaj sposób pracy')}"><button role="tab" id="tab-sampling" aria-selected="true" aria-controls="panel-sampling">SAMPLING</button><button role="tab" id="tab-sequencing" aria-selected="false" aria-controls="panel-sequencing" tabindex="-1">SEQUENCING</button></div>
    <div role="tabpanel" id="panel-sampling" aria-labelledby="tab-sampling" tabindex="0">{image('web/chop-current.jpg',t('CHOP with AUTO DETECT, cut markers and the selected waveform slice ready to audition.','CHOP z AUTO DETECT, znacznikami cięcia i zaznaczonym fragmentem do odsłuchu.'),1134,1510,'sampler-detail')}<p class="image-caption">AUTO DETECT · GRID · LIVE CHOP</p></div>
    <div role="tabpanel" id="panel-sequencing" aria-labelledby="tab-sequencing" tabindex="0" hidden>{image('web/note-length-current.jpg',t('Bank B sequencer with short and extended notes.','Sekwencer banku B z krótkimi i wydłużonymi nutami.'),1158,548)}<p class="image-caption">16 / 32 STEPS · PATTERN / SONG</p></div>
  </div><p class="workflow-note">{t('Load a file or record with the microphone. Find cuts with AUTO DETECT, divide the waveform with GRID, or tap in your own cuts with LIVE CHOP. Audition a slice on the waveform, then use ASSIGN TO PADS.','Wczytaj plik albo nagraj dźwięk mikrofonem. Znajdź cięcia przez AUTO DETECT, podziel waveform w GRID lub wstaw własne cięcia w LIVE CHOP. Odsłuchaj fragment na waveformie i użyj ASSIGN TO PADS.')}</p></div>
  <div class="capture-panels"><article><div class="panel-heading"><h3>GØ GRAB</h3>{pro()}</div>{image('web/grab-current.jpg',t('GØ GRAB capture panel with SAVE LAST 30s.','Panel GØ GRAB z przyciskiem SAVE LAST 30s.'),1122,777)}<p>{t('Keep up to the last 30 seconds made available by iOS. On older and newer iPhones, the app chooses a compatible capture method.','Zachowaj do 30 ostatnich sekund udostępnionych przez iOS. Aplikacja sama wybiera zgodną metodę przechwytywania — na starszych i nowszych iPhone’ach.')}</p></article>
  <article><div class="panel-heading"><h3>CRATE</h3>{pro()}</div>{image('web/crate-current.jpg',t('CRATE with source filters, search, folders and favourite recordings.','CRATE z filtrami źródeł, wyszukiwaniem, folderami i ulubionymi nagraniami.'),1122,1030)}<p>{t('Organize takes into folders and mark favourites. Filter by the original source, even when a take is inside a folder. Preview, trim and load into SAMPLER, SAMPLED or a TURNTABLE slot.','Porządkuj nagrania w folderach i oznaczaj ulubione. Filtruj według źródła także wtedy, gdy nagranie jest w folderze. Odsłuchaj, przytnij i wczytaj do SAMPLER, SAMPLED lub slotu TURNTABLE.')}</p></article></div>
  <p class="small-print">{t('GØ GRAB and CRATE require PRO. Capture only audio you own or have permission to use. Protected content and source apps may restrict recording.','GØ GRAB i CRATE wymagają PRO. Nagrywaj materiały, do których masz prawa lub zgodę. Aplikacje źródłowe i zabezpieczone treści mogą ograniczać przechwytywanie.')}</p>{guide('sampling','Sampling & capture guide','Sampling i przechwytywanie (EN)')}
</section>

<section class="section performance" id="performance" aria-labelledby="fx-title">
  <div class="feature-heading"><p class="eyebrow">03 / TONE FX + PERFORMANCE FX</p><h2 id="fx-title">SHAPE YOUR<br><span class="orange">SOUND.</span></h2><p class="section-description">{t('Texture in the sound. Movement in the performance. Put your hands on both.','Nadaj brzmieniu charakter. Dodaj ruch podczas grania. Wszystko pod palcami.')}</p></div>
  <div class="sound-fx-grid"><article><h3>TONE FX</h3>{image('web/tone-fx-current.jpg',t('Actual TONE FX: Vinyl Glue, Cassette, Vinyl Noise, Drive, Lo-Fi, Dirt Glitch and Pitch Mod.','TONE FX: Vinyl Glue, Cassette, Vinyl Noise, Drive, Lo-Fi, Dirt Glitch i Pitch Mod.'),1160,704)}<p>{t('Vinyl warmth, cassette colour, saturation and grit. Shape the character of the machine.','Ciepło winylu, kolor kasety, nasycenie i brud. Zbuduj własny charakter maszyny.')}</p><ul class="effect-list"><li>VINYL GLUE</li><li>CASSETTE</li><li>VINYL NOISE</li><li>DRIVE</li><li>LO-FI</li><li>DIRT GLITCH</li><li>PITCH MOD</li></ul></article>
  <article><h3>PERFORMANCE FX</h3>{image('web/performance-fx-current.jpg',t('Actual PERFORMANCE FX: Super Filter, Isolator, Tape Echo, Pitch All, Looper, Vinyl Stop and Mute Drums.','PERFORMANCE FX: Super Filter, Isolator, Tape Echo, Pitch All, Looper, Vinyl Stop i Mute Drums.'),1160,704)}<p>{t('Filter, echo and loop the beat live. Combine LOOPER with MUTE DRUMS. HOLD keeps the effect engaged.','Filtruj, zapętlaj i dodawaj echo na żywo. Łącz LOOPER z MUTE DRUMS. HOLD utrzyma efekt, gdy ręce zajmą się czymś innym.')}</p><ul class="effect-list"><li>SUPER FILTER</li><li>ISOLATOR</li><li>TAPE ECHO</li><li>PITCH ALL</li><li>LOOPER</li><li>MUTE DRUMS</li><li>VINYL STOP</li></ul></article></div>
  {guide('performance','Performance FX guide','PERFORMANCE FX w praktyce (EN)')}
</section>

<section class="section turntable-section" id="turntable" aria-labelledby="turntable-title"><span id="capture" class="anchor-alias"></span>
  <div class="turntable-layout"><div class="feature-heading"><p class="eyebrow">04 / GØ TURNTABLE</p><h2 id="turntable-title">CUT.<br>SCRATCH.<br><span class="orange">REPEAT.</span></h2><p class="section-description">{t('Load your own sound. Set speed, level and a cue for each slot, then work the platter and crossfader over your beat.','Załaduj własny dźwięk. Ustaw prędkość, głośność i punkt CUE każdego slotu. Scratchuj do bitu, używając talerza i crossfadera.')}</p><p class="turntable-motto">FREE TO SCRATCH.<br>PRO TO GO FURTHER.</p><dl class="slot-access"><div><dt>FREE</dt><dd>{t('2 scratch slots','2 sloty do scratchowania')}</dd></div><div><dt>PRO</dt><dd>{t('4 slots + record scratches','4 sloty + nagrywanie scratchy')}</dd></div></dl>{guide('turntable','Explore TURNTABLE','Poznaj TURNTABLE (EN)')}</div>
  {image('web/turntable-current.jpg',t('GØ TURNTABLE with four slots, cue waveform, GØ-404 vinyl label and crossfader.','GØ TURNTABLE z czterema slotami, waveformem z punktem CUE, etykietą winylu GØ-404 i crossfaderem.'),1206,2334,'turntable-detail')}</div>
</section>

<section class="section bass-section" id="instruments" aria-labelledby="bass-title">
  <div class="feature-heading"><p class="eyebrow">05 / BANK B · BASS &amp; INSTRUMENT</p><h2 id="bass-title">BRING THE<br><span class="orange">LOW END.</span></h2><p class="section-description">{t('Build a bassline. Find a melody. Make the whole beat yours.','Zbuduj linię basu. Znajdź melodię. Nadaj bitowi własny styl.')}</p></div>
  <div class="bass-layout"><div class="bass-media">
    <div class="tabs" role="tablist" aria-label="{t('Bank B sound sources','Źródła brzmienia banku B')}"><button role="tab" id="tab-b-synth" aria-selected="true" aria-controls="panel-b-synth">SYNTH</button><button role="tab" id="tab-b-sampled" aria-selected="false" aria-controls="panel-b-sampled" tabindex="-1">SAMPLED</button></div>
    <div role="tabpanel" id="panel-b-synth" aria-labelledby="tab-b-synth" tabindex="0">{image('web/bass-current.jpg',t('BASS editor showing the Analog Bass preset, Character and Octave.','Edytor BASS z presetem Analog Bass oraz kontrolkami Character i Octave.'),1119,1240,'bass-detail')}</div>
    <div role="tabpanel" id="panel-b-sampled" aria-labelledby="tab-b-sampled" tabindex="0" hidden>{image('web/sampled-current.jpg',t('SAMPLED editor with waveform, trim handles, octave and GATE.','Edytor SAMPLED z waveformem, uchwytami TRIM, oktawą i trybem GATE.'),750,1074,'bass-detail')}</div>
  </div><div class="bass-copy"><h3>{t('Play a synth.<br>Or play your own sample.','Zagraj na syntezatorze.<br>Albo na własnym samplu.')}</h3><p>{t('B1–B8 play bass and B9–B16 play instruments. Choose a SYNTH preset, or load one sound in SAMPLED and play it across the eight pads. Trim the waveform, set the root note and octave, and choose ONE SHOT or GATE.','B1–B8 to bas, B9–B16 to instrumenty. Wybierz preset SYNTH albo wczytaj dźwięk w SAMPLED i zagraj nim na ośmiu padach. Przytnij waveform, ustaw nutę bazową, oktawę i wybierz ONE SHOT lub GATE.')}</p><div class="inline-feature"><p class="eyebrow">SMART KEY</p><p>{t('Smart Key refreshes its key detection when the samples on A9–A16 change.','Smart Key ponawia analizę tonacji po zmianie sampli na A9–A16.')}</p></div>{guide('bank-b','Bass, instruments & Auto Key','Bas, instrumenty i Auto Key (EN)')}</div></div>
</section>

<section class="section vintage-section" id="vintage" aria-labelledby="vintage-title">
  <div class="feature-heading"><p class="eyebrow">06 / VINTAGE · RESAMPLING</p><h2 id="vintage-title">OLD SCHOOL.<br><span class="orange">NEW RULES.</span></h2><p class="section-description">{t('Three sampling characters. Your original source stays yours.','Trzy charaktery samplingu. Oryginalny materiał pozostaje nienaruszony.')}</p></div>
  <div class="vintage-layout">{image('web/flavor-current.jpg',t('FLAVOR in PAD EDIT with waveform, Vintage and the 1200, 60 and 3000 models.','Zakładka FLAVOR w PAD EDIT z waveformem, Vintage i modelami 1200, 60 oraz 3000.'),1119,2245,'vintage-detail')}
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
  <div class="resample-story"><div><p class="eyebrow">FLIP IT. RESAMPLE IT.</p><h3>{t('The performance<br>becomes the sample.','Z występu<br>powstaje nowy sampel.')}</h3><p>{t('Print a pattern, song or live pass with performance FX. In TAPES, browse your takes, trim on the waveform and export WAV or send the recording to a pad. Choose A1–A16 or RES. Green lights show free pads and yellow lights show occupied pads. Use RESAMPLE in PAD EDIT to print just one pad.','Zapisz pattern, song lub występ z PERFORMANCE FX. W TAPES przeglądaj nagrania, przycinaj je na waveformie, eksportuj WAV lub przypisz nagranie do pada. Wybierz A1–A16 lub RES. Zielone lampki wskazują wolne pady, żółte zajęte. Aby zapisać brzmienie pojedynczego pada, użyj RESAMPLE w PAD EDIT.')}</p>{guide('resampling','Resampling & TAPES','Resampling i TAPES (EN)')}</div>{image('web/tapes-current.jpg',t('TAPES with a take list, trim waveform, TO PAD and EXPORT WAV.','TAPES z listą nagrań, waveformem do przycinania oraz TO PAD i EXPORT WAV.'),740,910,'tapes-detail')}</div>
  <div class="edit-features"><article><h3>TIME STRETCH</h3><p>{t('Change length, keep the pitch. Drag the waveform handle or use FIT TO BPM. THIS PAD / ALL works within the current group of eight.','Zmień długość bez zmiany wysokości dźwięku. Przeciągnij uchwyt waveformu lub użyj FIT TO BPM. THIS PAD / ALL działa w bieżącej grupie ośmiu padów.')}</p>{guide('time-stretch','Stretch & Fit to BPM','Stretch i Fit to BPM (EN)')}</article><article><h3>SIDECHAIN</h3><p>{t('Let a chosen bank A pad make room in your samples, bass or instruments. Set amount and release, for one pad or the group.','Wybrany pad banku A robi miejsce w samplach, basie lub instrumentach. Ustaw Amount i Release dla jednego pada lub całej grupy.')}</p>{guide('sidechain','Sidechain guide','Jak używać SIDECHAIN (EN)')}</article></div>
</section>

<section class="section ownership" id="free-pro" aria-labelledby="ownership-title"><div class="feature-heading"><p class="eyebrow">07 / FREE &amp; PRO</p><h2 id="ownership-title">YOUR BEAT.<br><span class="orange">YOUR MACHINE.</span></h2><p class="section-description">{t('The core instrument stays free. PRO adds capture, a sample library and more ways to take your music further.','Podstawowa bitmaszyna jest darmowa. PRO dodaje przechwytywanie, bibliotekę sampli i więcej możliwości pracy z muzyką.')}</p></div><div class="comparison">'''
    free=[t('Unlimited local projects','Nieograniczone projekty lokalne'),t('Sampling, CHOP & per-pad editing','Sampling, CHOP i edycja padów'),t('16 / 32 steps, swing & Song Mode','16 / 32 kroki, swing i tryb Song'),t('Core FX, Vintage & resampling','Podstawowe FX, Vintage i resampling'),t('TURNTABLE: 2 scratch slots','TURNTABLE: 2 sloty do scratchowania'),t('Time Stretch, Sidechain & MIDI Learn','Time Stretch, Sidechain i MIDI Learn'),t('Bass & instrument voices','Bas i instrumenty'),t('WAV export','Eksport WAV'),t('Included drum kits & free faceplates','Fabryczne zestawy perkusji i darmowe faceplate’y')]
    premium=['GØ GRAB',t('CRATE & USB SAMPLING','CRATE i USB SAMPLING'),t('TURNTABLE: 4 slots + record scratches','TURNTABLE: 4 sloty + nagrywanie scratchy'),t('STEMS export','Eksport STEMS'),t('GØ BACKUP to your private iCloud','GØ BACKUP do prywatnego iCloud'),t('GØ TAPES drum pack','Pakiet perkusyjny GØ TAPES'),t('ANALOG ROOTS faceplate pack','Pakiet faceplate’ów ANALOG ROOTS')]
    for name,items,label in [('FREE',free,t('THE CORE INSTRUMENT','PODSTAWOWA MASZYNA')),('PRO',premium,t('GO FURTHER','WIĘCEJ MOŻLIWOŚCI'))]:
        body+=f'<article><div class="tier-heading"><h3>{name}</h3><span>{label}</span></div><ul>'+''.join(f'<li>{item}</li>'for item in items)+'</ul></article>'
    body+=f'''</div><p class="small-print">{t('PRO is a subscription. Plans and localized prices are shown by Apple in the app. Drum and faceplate packs sold separately remain separate purchases.','PRO jest subskrypcją. Plany i lokalne ceny pokazuje Apple w aplikacji. Pakiety perkusji i faceplate’ów sprzedawane osobno są niezależnymi zakupami.')}</p>
<div class="make-yours"><div><p class="eyebrow">MAKE IT YOURS.</p><h3>{t('Your sound.<br>Your front panel.','Twoje brzmienie.<br>Twoja obudowa.')}</h3><p>{t('Start with GØ DUST. Add GØ STREETS, GØ CRATES or your own samples. Pick a faceplate that feels like your machine.','Zacznij od GØ DUST. Sięgnij po GØ STREETS, GØ CRATES lub własne sample. Wybierz faceplate, który pasuje do Twojej maszyny.')}</p><p class="small-print">{t('Store availability will be confirmed at release.','Dostępność pakietów w sklepie zostanie potwierdzona na premierę.')}</p></div><div class="faceplate-gallery" aria-label="{t('Three real faceplate designs','Trzy prawdziwe wersje wyglądu')}">'''
    for name,file,label in [('ORANGE DUST','orange-dust',t('FREE DESIGN','DARMOWY WZÓR')),('RAW METAL','raw-metal',t('FREE DESIGN','DARMOWY WZÓR')),('SOUL CONSOLE','soul-console',t('PRO DESIGN','WZÓR PRO'))]:
        body+=f'<div>{image("web/faceplate-"+file+"-current.jpg",t("Actual GØ-404 with the ","Prawdziwa GØ-404 z faceplate’em ")+name,780,1688)}<p class="image-caption">{name}<span>{label}</span></p></div>'
    body+=f'''</div></div></section>

<section class="section connections" id="connections" aria-labelledby="connections-title"><div class="feature-heading"><p class="eyebrow">08 / {t('CONNECT. SAVE. KEEP CREATING.','PODŁĄCZ. ZAPISZ. TWÓRZ DALEJ.')}</p><h2 id="connections-title">{t('BEYOND<br><span class="orange">THE PADS.</span>','WIĘCEJ<br><span class="orange">NIŻ PADY.</span>')}</h2></div><div class="tool-list">'''
    tools=[('USB SAMPLING',True,'usb',t('Record compatible external audio by USB‑C or a Lightning USB host adapter. Check the input, REC, then STOP → CRATE. USB audio compatibility varies; it is separate from MIDI.','Nagrywaj ze zgodnego wejścia audio przez USB‑C lub adapter USB host do Lightning. Sprawdź wejście, naciśnij REC, potem STOP → CRATE. Zgodność zależy od sprzętu; USB audio i MIDI to osobne funkcje.')),
           ('MIDI LEARN',False,'midi',t('Connect a controller by USB‑C or Lightning USB host adapter. Open SETTINGS → MIDI LEARN to map pads, buttons and knobs. Your assignments are saved.','Podłącz kontroler przez USB‑C lub adapter USB host do Lightning. Otwórz SETTINGS → MIDI LEARN, aby przypisać pady, przyciski i gałki. Aplikacja zapamięta mapowanie.')),
           ('DISPLAY',False,'display',t('Set PAD LIGHTS and PAD PRESS separately in SETTINGS → DISPLAY. On iPad, the same panel lets you choose CLASSIC or iPAD FIT.','W SETTINGS → DISPLAY ustaw osobno PAD LIGHTS i PAD PRESS. Na iPadzie w tym panelu wybierzesz też CLASSIC lub iPAD FIT.')),
           ('WAV / STEMS',False,'export',t('Export a pattern, song or RES as WAV. PRO adds separate stems for mixing.','Eksportuj pattern, song lub RES do WAV. PRO dodaje osobne ślady do miksowania.')),
           ('GØ BACKUP',True,'backup',t('Choose PROJECTS or CRATE and select what to keep in iCloud. In BACKUP use UPLOAD; in RESTORE use DOWNLOAD. Uploading requires PRO. Existing cloud backups can still be restored after PRO ends.','Wybierz PROJECTS lub CRATE i zaznacz materiały, które chcesz zachować w iCloud. W BACKUP użyj UPLOAD, a w RESTORE — DOWNLOAD. Wysyłanie wymaga PRO. Istniejące kopie można przywrócić także po wygaśnięciu PRO.')),
           (t('PROJECTS & FOLDERS','PROJEKTY I FOLDERY'),False,'projects',t('Save, overwrite or create a new copy. Organize projects into your own folders when you need them.','Zapisz projekt, nadpisz go lub utwórz nową kopię. Organizuj bity we własnych folderach, jeśli tego potrzebujesz.'))]
    for name,premium_,anchor,copy in tools:
        body+=f'<article><div class="tool-name"><h3>{name}</h3>{pro()if premium_ else""}</div><div><p>{copy}</p>{guide(anchor,"Explore the workflow","Zobacz, jak to działa (EN)")}'
        if anchor == 'backup':
            body+=image('web/backup-current.jpg',t('GØ BACKUP in RESTORE mode with cloud backups and DOWNLOAD.','GØ BACKUP w trybie RESTORE z listą CLOUD BACKUPS i przyciskiem DOWNLOAD.'),730,1575,'backup-detail')
        body+='</div></article>'
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
