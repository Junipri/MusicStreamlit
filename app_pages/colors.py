import colorsys
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Optional

import numpy as np
import streamlit as st
import matplotlib as mpl
from matplotlib import pyplot as plt, patches

from enums.notes import get_piano_notes, NoteNames, Note, get_piano_note_chord_color_patches

st.header("Colors")

NUM_OCTAVES = 9
NUM_NOTES = 12


def get_note_color_bar_chart():
    # Create RGB image array
    white = (255, 255, 255)
    img = np.full((NUM_OCTAVES, NUM_NOTES, 3), white)

    for piano_note in get_piano_notes():
        pos = piano_note.octave, piano_note.name.idx
        img[pos] = piano_note.get_rgb(_255=True)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.imshow(img, interpolation='none')

    # Ticks and labels
    ax.set_yticks(np.arange(NUM_OCTAVES))
    ax.set_yticklabels(list(range(NUM_OCTAVES)))

    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    ax.set_xticks(np.arange(NUM_NOTES))
    ax.set_xticklabels(NoteNames)

    # Draw gridlines
    ax.set_yticks(np.arange(-0.5, NUM_OCTAVES, 1), minor=True)
    ax.set_xticks(np.arange(-0.5, NUM_NOTES, 1), minor=True)
    ax.grid(which='minor', color='black', linewidth=1)
    ax.tick_params(which='minor', bottom=False, left=False)

    st.pyplot(fig, use_container_width=False)


get_note_color_bar_chart()
