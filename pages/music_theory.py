import librosa
import numpy as np
import streamlit as st
from matplotlib import pyplot as plt

from enums.notes import NotesNames, ChordTypes, get_tone, get_piano_notes, Note
from enums.common import Octaves


def notes_section():
    st.header(
        "Chords",
        divider='rainbow'
    )

    st.subheader(
        "Chord Types",
        divider='violet'

    )

    selected_note: Note = st.radio(
        label="Notes",
        options=get_piano_notes(),
        format_func=lambda note: str(note),
        horizontal=True
    )
    ChordTypes.radio(label="Chord Types")
    selected_chord_type = ChordTypes.get_radio()

    chord = selected_note.get_chord(chord_type=selected_chord_type)

    chord_tones = [get_tone(n.frequency) for n in chord]
    T, S = zip(*chord_tones)
    chord_sig = np.sum(S, axis=0)

    periods = [n.period for n in chord]
    max_period = max(periods) * 12

    fig, ax = plt.subplots(figsize=(10, 4))

    colors = ['red', 'blue', 'green']
    for i, (t, s) in enumerate(chord_tones):
        ax.plot(t, s, color=colors[i], label=str(chord[i]), alpha=0.2)
    ax.plot(T[0], chord_sig, color='orange')
    fig.legend()
    ax.set_xlim(0, max_period)

    st.pyplot(fig)
    st.audio(chord_sig, sample_rate=44100, autoplay=True)


notes_section()
