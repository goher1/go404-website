"""Static landing page reached only after Brevo handles the confirmation token."""
from pathlib import Path

def confirmation_page(lang='en'):
    pl = lang == 'pl'
    title = 'Jesteś na liście.' if pl else 'You’re in.'
    description = 'Twój adres e-mail został potwierdzony.' if pl else 'Your email is confirmed.'
    detail = 'Wiadomości o nowych funkcjach, aktualizacjach i premierach GØ-404 będą trafiać do Twojej skrzynki.' if pl else 'Look out for GØ-404 features, updates and release news in your inbox.'
    home = '/pl/' if pl else '/'
    back = 'WRÓĆ DO GØ-404' if pl else 'BACK TO GØ-404'
    privacy = '/pl/privacy/' if pl else '/privacy/'
    legal = 'Polityka prywatności' if pl else 'Privacy Policy'
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><meta name="color-scheme" content="dark"><title>{title} — GØ-404 NEWS</title><link rel="icon" href="/assets/favicon.png"><link rel="stylesheet" href="/assets/news-confirmation.css"></head><body><main><a class="brand" href="{home}" aria-label="GØ-404"><img src="/assets/go404-logo.jpg" width="600" height="152" alt="GØ-404"></a><p class="eyebrow">GØ-404 NEWS</p><h1>{title}</h1><p class="confirmed">{description}</p><p class="detail">{detail}</p><a class="button" href="{home}">{back}</a><footer><a href="{privacy}">{legal}</a><nav aria-label="Language"><a href="/news/confirmed/" lang="en" {'aria-current="page"' if not pl else ''}>EN</a><span> / </span><a href="/pl/news/confirmed/" lang="pl" {'aria-current="page"' if pl else ''}>PL</a></nav></footer></main></body></html>'''

def write_confirmation(site):
    for lang,route in [('en','news/confirmed'),('pl','pl/news/confirmed')]:
        out=Path(site)/'docs'/route
        out.mkdir(parents=True,exist_ok=True)
        (out/'index.html').write_text(confirmation_page(lang))
