# SEI Fit Map

A single, shareable web page that shows **two SEI Boston job descriptions exactly as posted** — Concept to Delivery Consultant and Strategy and Operations Consultant, switchable via tabs at the top — and lets a reader hover any highlighted phrase (it visibly becomes clickable) and click it to see the **specific, real experience** that backs it.

The intent: hand a hiring manager one link that proves fit, phrase by phrase, without them ever seeing anything behind the curtain.

It's employer-facing on purpose. There is **no internal language** on the page — no "match strength," no source tags, no gap notes. Every highlighted phrase simply opens the evidence behind it.

---

## Editing the copy — you only ever touch the content, never the code

Everything on the page (the JD text, the highlighted phrases, and the evidence behind each one) comes from **`data.json`**, which the page loads at runtime. Nothing is hardcoded in the HTML or JavaScript. To change wording, you change the content — not the code.

There are two equally valid ways to edit:

### Option A — edit `data.json` directly
Open `data.json` and edit the text. It's the file the page actually reads.

### Option B — edit `build_data.py`, then regenerate (recommended if you're comfortable)
`build_data.py` is a friendlier, commented layout of the same content. Edit it, then run:
```bash
python3 build_data.py
```
That rewrites `data.json` for you and prints a sanity check (phrase count + any broken evidence links). Use this if you want the evidence written right next to the phrase it backs.

### How the content is organized

- **`evidence`** — a dictionary of your accomplishments, shared by both roles. Each has a `title`, a `text`, and (for portfolio pieces) a `link`. One piece of evidence can back many phrases, in either role.
- **`roles`** — one entry per tab. Each role has an `id`, a `tab_label`, a `job` block, and its own `jd_prose`:
  - **`job`** — the role title, location, the link to the job board, the browser-tab title, and the short "Ryan Hance · Fit Map" framing line at the top.
  - **`jd_prose`** — the job description itself, in order, as a list of blocks:
    - `{"type": "p", ...}` — a paragraph
    - `{"type": "h2"/"h3", "text": "..."}` — a section heading
    - `{"type": "li", ...}` — a bullet
    - Inside a paragraph or bullet, plain text is just text; a **highlighted phrase** is an object with its own `text` and an `evidence` list of ids. That's what becomes clickable. Phrase ids must be unique across both roles (deep links use them to pick the right tab).

**To add a new proof point:** add an entry to `evidence`, then add its id to the `evidence` list of whichever phrase(s) it backs. It shows up automatically — no code change.

---

## What's on the page

- **Two tabs**, one per SEI role, each showing that posting's real text: **WHO WE LOOK FOR**, **WHAT WE DO**, and **QUALIFICATIONS** — styled to feel like SEI's own site (logo, ivory-and-ink palette, serif headlines, signature red accents). Each tab's "View the live posting" link goes to that role's posting.
- **Highlighted phrases** you can hover (they show a "clickable" cue) and click.
- A **side panel** (right on desktop, a bottom sheet on phones) that opens with the evidence behind the clicked phrase — an accomplishment title, the story, and a link to the case study when there is one.
- A **shareable deep link:** click a phrase and the address bar updates (e.g. `…/#p-tech-savvy`); sending that link opens the page on the right tab with that phrase already expanded. A bare role id (e.g. `…/#so`) opens that tab.

---

## Running it on your own computer

⚠️ **Don't double-click `index.html`.** The page loads its content with `fetch()`, which browsers block on the `file://` protocol, so opening the file directly shows an error. Serve it over http instead:

```bash
# from inside this folder:
python3 serve.py 8000
# then open http://localhost:8000/ in your browser
```
(or `python3 -m http.server 8000` — same result.)

---

## Publishing it as a shareable link (GitHub Pages)

GitHub Pages serves over https, so everything works there with no changes.

1. **Create a repo and push these files to its root:**
   ```bash
   cd sei-brainmap
   git init
   git add index.html styles.css app.js data.json sei-logo.svg README.md build_data.py
   git commit -m "SEI fit map"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
2. **Turn on Pages:** on GitHub → **Settings → Pages** → **Source: Deploy from a branch**, **Branch: `main`**, **Folder: `/ (root)`** → **Save**.
3. **Wait ~1 minute**, then open the URL Pages gives you:
   ```
   https://<your-username>.github.io/<repo-name>/
   ```
   That's the link you send. Deep links work too, e.g. `…/#p-design-thinking`.

---

## Files

```
sei-brainmap/
  index.html          # page structure (no content)
  styles.css          # SEI brand styling + responsive
  app.js              # loads data.json and renders the page
  data.json           # ALL content — the file the page reads
  build_data.py       # optional friendly editor that regenerates data.json
  sei-logo.svg        # SEI logo (original brand colors)
  serve.py            # optional local server (not needed on Pages)
  README.md           # this file
```

## Portfolio links

The six portfolio pieces link to their public **hance.work** case-study pages. To change one, edit that evidence item's `link` in `data.json` (or `build_data.py`).
