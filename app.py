import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="North Facing Home — Interior Design Plan",
    page_icon="🏠",
    layout="wide",
)

# Load the self-contained HTML/CSS/JS floor plan and embed it as-is.
html_path = Path(__file__).parent / "interior_design_plan.html"
html_content = html_path.read_text(encoding="utf-8")

st.components.v1.html(html_content, height=1150, scrolling=True)
