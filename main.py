from enum import Enum

import streamlit as st


class Pages(Enum):
    LIGHTSABERS = st.Page(
        page='pages/lightsabers.py',
        title='Lightsabers!'
    )
    MUSIC_THEORY = st.Page(
        page='pages/music_theory.py',
        title='Music Theory',
        icon='🎶'
    )

    COLORS = st.Page(
        page='pages/colors.py',
        title='Colors'
    )


def display_navigation():
    pg = st.navigation({"Pages": [_.value for _ in Pages]})
    pg.run()


st.set_page_config(layout="wide")
display_navigation()
