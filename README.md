# North Facing Home — Interior Design Plan (Streamlit)

A Streamlit wrapper around the interactive floor plan (SVG + HTML/CSS/JS embedded via `st.components.v1.html`).

## Files
- `app.py` — Streamlit entry point
- `interior_design_plan.html` — the floor plan itself (must stay in the same folder as `app.py`)
- `requirements.txt` — dependencies

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Then open the URL Streamlit prints (usually http://localhost:8501).

## Deploy on Streamlit Community Cloud (free)
1. Create a new GitHub repo and push these three files to it (keep them in the same folder, e.g. the repo root).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **New app**, pick the repo/branch, and set the main file path to `app.py`.
4. Click **Deploy**. Streamlit Cloud installs `requirements.txt` automatically and gives you a public URL.

## Deploy elsewhere (Render, Railway, an EC2 box, etc.)
Any host that can run:
```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```
will work, since there's no database or external API — just the two files above.

## Notes
- If you swap in a different HTML file, keep the filename referenced in `app.py` (`interior_design_plan.html`) in sync, or just rename the variable.
- The `height=1150` in `app.py` controls how tall the embedded plan renders — adjust if content gets cut off or leaves extra whitespace on your screen size.
