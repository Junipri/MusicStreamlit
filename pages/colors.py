import colorsys
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint

import numpy as np
import streamlit as st
import matplotlib as mpl
from matplotlib import pyplot as plt, patches

from enums.notes import get_piano_notes, NotesNames, Note

st.header("Colors")

hue = st.slider(label="Hue", min_value=0.0, max_value=1.0)
saturation = st.slider(label="saturation", min_value=0.0, max_value=1.0)
value = st.slider(label="value", min_value=0.0, max_value=1.0)

hsv = hue, saturation, value
st.write(f"hsv: {hsv}")

rgb = colorsys.hsv_to_rgb(*hsv)

st.subheader("bar chart?")

notes = [
    Note(name=note_name, octave=octave)
    for note_name in NotesNames
    for octave in range(0, 9)
]

data_dicts = [
    {
        "note": note.name.value,
        "octave": note.octave,
        "hue": note.name.hue,
        "h": 1
    }
    for note in notes
]

print(bar_colors.shape)

print(len(data_dicts))




st.bar_chart(data_dicts,
             x="h",
             x_label="octave",
             y="note",
             y_label="note",
             color=bar_colors)
st.write(data_dicts)
