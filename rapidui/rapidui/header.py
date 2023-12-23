import streamlit as st
from rapidui.lib import constants
from pathlib import Path

GLOBAL_CSS_PATH = Path(__file__).parent / "app.css"
CARDFILL_CSS_PATH = Path(__file__).parent / "cardfill.css"


def page_config_and_style(page_title: str, disable_card_fill: bool):
    st.set_page_config(
        page_icon="https://armandmcqueenpublic.blob.core.windows.net/centrality-public/favicon.ico",
        page_title=f"{page_title} | Centrality",
    )

    # Load app.css as a string and render it as markdown
    css_as_str = GLOBAL_CSS_PATH.read_text()
    st.markdown(f"<style>{css_as_str}</style>", unsafe_allow_html=True)

    if not disable_card_fill:
        card_fill_css_as_str = CARDFILL_CSS_PATH.read_text()
        st.markdown(f"<style>{card_fill_css_as_str}</style>", unsafe_allow_html=True)


def mini_logo():
    # TODO: Probably don't need styling for both a and img here
    mini_logo_html = f"""
                <div style='display: flex'>
                    <a href="/" target="_self" class="logo">
                        <img src='{constants.LOGO_SVG}' class="logo">
                    </a>
                    <p class="logo-name">Centrality</p>
                </div>
                """
    st.markdown(mini_logo_html, unsafe_allow_html=True)


def header(page_title: str, disable_card_fill: bool = False):
    page_config_and_style(page_title, disable_card_fill=disable_card_fill)
    mini_logo()
    st.markdown(
        f"""<h2 class="page-title">{page_title}</h1>""",
        unsafe_allow_html=True,
    )
    st.divider()
