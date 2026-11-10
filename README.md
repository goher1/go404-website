# GØ-404 official website

Standalone HTML, CSS and JavaScript for https://go404.app. This repository contains only the public website, its website generator, content, artwork and font licenses. The music application source and its history are not included.

## Edit and preview

- Text and page structure: `tools/build.py`.
- Support guides: `content/support.json`.
- Approved Privacy Policy: `content/privacy-policy.html`; substantive changes require the owner's approval.
- Styling and interactions: `docs/assets/site.css`, `docs/assets/site.js`, `docs/support/support.css` and `docs/support/support.js`.
- Images and fonts: `docs/assets/`.
- Canonical origin, contact and App Store URL: `site.config.json`.

Python 3 is the only generator requirement; there are no packages to install. After edits, run `python3 tools/build.py`. Preview with `python3 -m http.server 4180 --bind 127.0.0.1 --directory docs`, then open http://127.0.0.1:4180/.

## Publish after owner approval

GitHub Pages source: `main` / `docs`. Commit the source and generated files together, then push. GitHub's built-in Pages deployment publishes that folder. No custom Actions workflow or paid runner is required. Never add application source, credentials, local audit files or private Git history.

The custom domain is `go404.app`; `docs/CNAME` must stay in every update. The DNS setup is retained when content changes. Enable Enforce HTTPS in Pages settings once GitHub has issued the certificate. GitHub Pages does not use the Cloudflare-style `_headers` file produced by the generator; no server-header enforcement is claimed here.

The App Store badge stays disabled until an official public App Store URL is confirmed. The original policy at https://goher1.github.io/go404-privacy/ is retained independently.
