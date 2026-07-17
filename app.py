import base64
import streamlit as st
from pathlib import Path
from openai import OpenAI

st.set_page_config(
    page_title="North Facing Home — Interior Design Plan",
    page_icon="🏠",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Room + style data (mirrors the floor plan's palette presets and room info)
# ---------------------------------------------------------------------------
ROOM_INFO = {
    "Kitchen":        {"dims": "8' x 8'",        "floor": "vitrified anti-skid tile",              "wall": "warm putty finish with an oil-proof glass backsplash", "furniture": "an L-shaped counter, a 2-burner hob, a single-bowl sink, overhead cabinetry"},
    "Attached Toilet":{"dims": "4' x 4'6\"",      "floor": "matte ceramic tile",                     "wall": "aqua-tinted tile dado to 4 feet, waterproof paint above", "furniture": "a wall-hung WC and a corner wash basin"},
    "Store Room":     {"dims": "4' x 4'",         "floor": "plain ceramic tile",                     "wall": "durable enamel paint",                                 "furniture": "three fixed utility shelves floor to ceiling"},
    "Puja Room":      {"dims": "4' x 3'",         "floor": "marble or light stone inlay",            "wall": "soft ivory with a wooden mandir backdrop",             "furniture": "a compact wall-mounted mandir with a small shelf below"},
    "Master Bedroom": {"dims": "10' x 16'6\"",    "floor": "engineered wood laminate",               "wall": "a soft clay accent wall behind the headboard, warm white elsewhere", "furniture": "a king bed with an upholstered headboard, two nightstands, an area rug, a reading chair"},
    "Dining":         {"dims": "8' x 8'",         "floor": "tile matching the adjoining kitchen",    "wall": "warm neutral tone, open to the hall",                  "furniture": "a 4-seat dining table with a pendant light above"},
    "Living Hall":    {"dims": "17' x 10'",       "floor": "large-format marble or vitrified tile",  "wall": "warm neutral with one textured feature wall behind the TV", "furniture": "a 3-seat sofa, a coffee table, a TV console, an area rug"},
    "Staircase":      {"dims": "leading to upper floor", "floor": "anti-skid stone treads",          "wall": "feature paint or exposed brick along the stair wall",  "furniture": "a wood or matte-black metal handrail"},
    "Car Parking":    {"dims": "9'6\" x 22'",     "floor": "broom-finish exposed-aggregate concrete","wall": "open to the driveway with a low garden wall",          "furniture": "a wall-mounted tool shelf and a weatherproof light"},
}

STYLE_DESCRIPTORS = {
    "Warm Contemporary": "warm contemporary Indian home interior, soft neutral and terracotta tones, brass accents, natural wood",
    "Coastal Minimal":   "coastal minimal interior, airy whites and soft seafoam greens, light oak wood, linen textures, abundant natural light",
    "Traditional Indian":"traditional Indian interior, warm ochre and teak tones, carved wood details, brass fixtures, rich textiles",
}

MODEL_OPTIONS = {
    "DALL·E 3 (recommended, widely available)": "dall-e-3",
    "gpt-image-1 (newer, needs org verification)": "gpt-image-1",
}

# ---------------------------------------------------------------------------
# Floor plan (unchanged — the SVG diagram)
# ---------------------------------------------------------------------------
st.title("North Facing Home — Interior Design Plan")

html_path = Path(__file__).parent / "interior_design_plan.html"
html_content = html_path.read_text(encoding="utf-8")
st.components.v1.html(html_content, height=1150, scrolling=True)

st.divider()

# ---------------------------------------------------------------------------
# AI render generator
# ---------------------------------------------------------------------------
st.header("🎨 Generate a Photorealistic Render")
st.caption("Pick a room and a style — this calls OpenAI's image API to generate an actual rendered photo, separate from the diagram above.")

if "gallery" not in st.session_state:
    st.session_state.gallery = []

with st.sidebar:
    st.subheader("OpenAI settings")
    api_key = st.text_input(
        "OpenAI API key",
        type="password",
        help="Get one at platform.openai.com/api-keys. For a deployed app, set this as a Streamlit secret instead (see README) so you don't have to paste it every visit.",
        value=st.secrets.get("OPENAI_API_KEY", "") if hasattr(st, "secrets") else "",
    )
    model_label = st.selectbox("Model", list(MODEL_OPTIONS.keys()))
    model = MODEL_OPTIONS[model_label]
    st.caption("DALL·E 3 images cost roughly $0.04–$0.08 each depending on size/quality.")

col1, col2 = st.columns(2)
with col1:
    room = st.selectbox("Room", list(ROOM_INFO.keys()))
with col2:
    style = st.selectbox("Style", list(STYLE_DESCRIPTORS.keys()))

extra_notes = st.text_area(
    "Extra styling notes (optional)",
    placeholder="e.g. add a ceiling fan, use blue accent cushions, view from the doorway",
)

def build_prompt(room_name, style_name, extra):
    info = ROOM_INFO[room_name]
    prompt = (
        f"A photorealistic, professionally lit interior design photograph of a "
        f"{style_name.lower()} {room_name.lower()} in an Indian home, "
        f"{info['dims']} in size. "
        f"Flooring: {info['floor']}. Walls: {info['wall']}. "
        f"Furniture and fixtures: {info['furniture']}. "
        f"Overall design direction: {STYLE_DESCRIPTORS[style_name]}. "
        f"Wide-angle interior photography, magazine quality, warm ambient lighting, "
        f"no people, no text, no watermark."
    )
    if extra.strip():
        prompt += f" Additional notes: {extra.strip()}."
    return prompt

generate = st.button("Generate render", type="primary", disabled=not api_key)
if not api_key:
    st.info("Enter your OpenAI API key in the sidebar to enable generation.")

if generate:
    prompt = build_prompt(room, style, extra_notes)
    with st.spinner(f"Generating {style} {room}..."):
        try:
            client = OpenAI(api_key=api_key)
            kwargs = dict(model=model, prompt=prompt, size="1024x1024", n=1)
            if model == "dall-e-3":
                kwargs["quality"] = "standard"
                kwargs["response_format"] = "b64_json"
            result = client.images.generate(**kwargs)
            b64 = result.data[0].b64_json
            image_bytes = base64.b64decode(b64)

            st.session_state.gallery.insert(0, {
                "room": room,
                "style": style,
                "prompt": prompt,
                "image": image_bytes,
            })
        except Exception as e:
            st.error(f"Image generation failed: {e}")

if st.session_state.gallery:
    latest = st.session_state.gallery[0]
    st.subheader(f"{latest['style']} — {latest['room']}")
    st.image(latest["image"], use_container_width=True)
    st.download_button(
        "Download this render",
        data=latest["image"],
        file_name=f"{latest['room'].replace(' ', '_').lower()}_{latest['style'].replace(' ', '_').lower()}.png",
        mime="image/png",
    )
    with st.expander("Prompt used"):
        st.code(latest["prompt"])

if len(st.session_state.gallery) > 1:
    st.subheader("Previous renders")
    cols = st.columns(4)
    for i, item in enumerate(st.session_state.gallery[1:], start=1):
        with cols[(i - 1) % 4]:
            st.image(item["image"], caption=f"{item['style']} — {item['room']}", use_container_width=True)
