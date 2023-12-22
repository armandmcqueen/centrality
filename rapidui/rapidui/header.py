import streamlit as st
from rapidui.lib import constants
from pathlib import Path

CSS_PATH = Path(__file__).parent / "app.css"
CARDFILL_CSS_PATH = Path(__file__).parent / "cardfill.css"


def page_config_and_style(page_title: str, disable_card_fill: bool):
    st.set_page_config(
        page_icon="https://armandmcqueenpublic.blob.core.windows.net/centrality-public/favicon.ico",
        page_title=f"{page_title} | Centrality",
    )

    # Load app.css as a string and render it as markdown
    css_as_str = CSS_PATH.read_text()
    st.markdown(f"<style>{css_as_str}</style>", unsafe_allow_html=True)

    if not disable_card_fill:
        card_fill_css_as_str = CARDFILL_CSS_PATH.read_text()
        st.markdown(f"<style>{card_fill_css_as_str}</style>", unsafe_allow_html=True)


def mini_logo():
    mini_logo_style = "display: block; margin-left: 0; width: 34px; "
    # TODO: Move styling to app.css with class/id
    mini_logo_html = f"""
                <div style='display: flex'>
                    <a href="/" target="_self" style='{mini_logo_style}'>
                        <img src='{constants.LOGO_SVG}' style='{mini_logo_style}'>
                    </a>
                    <p style='text-align: left; padding-top: 8px; padding-left: 10px; font-size: 15px;'>Centrality</p>
                </div>
                """
    st.markdown(mini_logo_html, unsafe_allow_html=True)


def header(page_title: str, disable_card_fill: bool = False):
    page_config_and_style(page_title, disable_card_fill=disable_card_fill)
    mini_logo()
    st.markdown(
        f"<h2 style='text-align: center;'>{page_title}</h1>",
        unsafe_allow_html=True,
    )
    st.divider()

