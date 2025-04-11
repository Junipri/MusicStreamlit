from collections import defaultdict
from pprint import pprint

import librosa
import streamlit as st
from matplotlib import pyplot as plt

from enums.notes import get_piano_notes, Note, NotesNames, get_piano_note_harmonics
from utils.common import adsr_envelope

note_to_octaves_map = defaultdict(list)
octave_to_notes_map = defaultdict(list)

piano_notes = get_piano_notes()

for note in piano_notes:
    note_to_octaves_map[note.name].append(note.octave)
    octave_to_notes_map[note.octave].append(note.name)

st.header("Lightsabers")

selected_note: NotesNames = st.radio(
    label="Notes",
    options=list(NotesNames),
    index=0,
    format_func=lambda note_name: note_name.value,
    horizontal=True
)

selected_octave: int = st.radio(
    label="Octaves",
    options=list(range(9)),
    index=4,
    horizontal=True
)

note = Note(name=selected_note, octave=selected_octave)
st.subheader(f"Note: {note} ( {note.frequency:,.2f}hz )")

t, note_signal = get_piano_note_harmonics(note, 1)
note_signal = note_signal[0, :]

note_enveloped = adsr_envelope(
    audio_signal=note_signal,
    attack_percent=0.005,
    decay_percent=.005,
    sustain_amplitude=0.7,
    release_percent=0.7
)
fig, ax = plt.subplots()
ax.plot(t, note_signal)
st.pyplot(fig)

st.audio(data=note_signal, autoplay=True, sample_rate=44100)

print(selected_octave)
