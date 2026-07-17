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

## AI-generated room renders (new)
Below the diagram, the app now has a section that calls OpenAI's image API to generate an actual photorealistic photo of any room, in any of the three styles.

### Get an OpenAI API key
1. Go to https://platform.openai.com/api-keys and sign in (you'll need billing set up on the account — image generation is pay-per-image, roughly $0.04–$0.08 each with DALL·E 3).
2. Click **Create new secret key**, copy it (you won't be able to see it again).

### Use it locally
Paste the key into the sidebar field when the app is running. It's only kept in that browser session, not saved anywhere.

### Use it on Streamlit Community Cloud (so you don't paste it every time)
1. In your deployed app, click **⋮ → Settings → Secrets**.
2. Add:
   ```toml
   OPENAI_API_KEY = "sk-...your key..."
   ```
3. Save. The app will pick it up automatically and pre-fill the sidebar field.

**Never commit your API key into the GitHub repo itself** — always use Streamlit's Secrets manager or paste it in the sidebar at runtime.
