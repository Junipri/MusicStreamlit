from __future__ import annotations

import colorsys
from dataclasses import dataclass
from enum import Enum
from functools import cache

import librosa
import numpy as np
import tabulate

from enums.common import _Radioable
from utils.common import color_text


class ScaleTypes(_Radioable):
    MAJOR = (2, 2, 1, 2, 2, 2, 1)
    MINOR = (2, 1, 2, 2, 1, 2, 2)


class ChordTypes(_Radioable):
    @classmethod
    def radio_format_func(cls, item: Enum, *_) -> str:
        return super().radio_format_func(item, use_value=False)

    def __str__(self):
        return str(self.name).capitalize()

    def __repr__(self):
        return str(self)

    MAJOR = (0, 4, 7)
    MINOR = (0, 3, 7)
    DIMINISHED = (0, 3, 6)
    AUGMENTED = (0, 4, 8)


def get_tone(frequency: float, duration: float = 1.0, sample_rate: float = 44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave = np.sin(2 * np.pi * frequency * t)
    return t, sine_wave


def get_piano_note_harmonics(note: Note, duration_in_seconds: float, sample_rate: int = 44100):
    t = np.linspace(0, duration_in_seconds, int(duration_in_seconds * sample_rate), endpoint=False)

    harmonic_amplitudes = [
        0.6,
        0.4,
        0.2
    ]

    signal = note.get_tone() + np.sum(
        [
            note.get_octave(d_octave).get_tone()[1] * amplitude
            for d_octave, amplitude in enumerate(harmonic_amplitudes, start=1)
        ]
    )
    return t, signal


class NotesNames(_Radioable):
    C = "C"
    C_SHARP = "C#"
    D = "D"
    D_SHARP = "D#"
    E = "E"
    F = "F"
    F_SHARP = "F#"
    G = "G"
    G_SHARP = "G#"
    A = "A"
    A_SHARP = "A#"
    B = "B"

    @property
    def idx(self) -> int:
        return list(NotesNames).index(self)

    @property
    def hue(self):
        return (((self.idx + 1) % 12) / 12) * 0.9


@dataclass
class Note:
    name: NotesNames = NotesNames.C
    octave: int = 4

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.name == other.name and self.octave == other.octave

    def __str__(self):
        return f"{self.name.value}{self.octave}"

    def __repr__(self):
        return f"{str(self)} ( {self.frequency: ,.2f} Hz )"

    @property
    def frequency(self) -> float:
        return float(librosa.note_to_hz(str(self)))

    @property
    def period(self):
        return 1 / self.frequency

    @property
    def hls(self):
        def octave_to_lightness(
                octave: int,
                l_clamp: tuple[float, float] = (0.1, 0.9)
        ) -> float:
            # Assumes octaves 0 through 8
            l_min, l_max = l_clamp
            d_l = l_max - l_min
            return l_min + octave * d_l / 9

        hue = self.name.hue
        lightness = octave_to_lightness(octave=self.octave)
        saturation = 1

        return hue, lightness, saturation

    def get_rgb(self, _255: bool = False):
        rgb = colorsys.hls_to_rgb(*self.hls)
        if _255:
            rgb = (round(_ * 255) for _ in rgb)
        return tuple(rgb)

    def get_rgb_patch(self):
        return color_text(text="▒▒", rgb=self.get_rgb(_255=True))

    def get_tone(self):
        return get_tone(frequency=self.frequency)

    def get_octave(self, d: int = 1):
        return Note(name=self.name, octave=self.octave + d)

    def get_chord(self, chord_type: ChordTypes = ChordTypes.MAJOR):
        piano_notes: list[Note] = get_piano_notes()

        root_idx = [i for i, n in enumerate(piano_notes) if str(self) == str(n)][0]
        chord = [piano_notes[root_idx + i] for i in chord_type.value]
        return chord


@cache
def get_piano_notes() -> list[Note]:
    p1 = [Note(name=n, octave=0) for n in [NotesNames.A, NotesNames.A_SHARP, NotesNames.B]]
    p2 = [Note(name=n, octave=o) for o in range(1, 8) for n in NotesNames]
    p3 = [Note(name=NotesNames.C, octave=8)]
    return p1 + p2 + p3


def get_piano_note_color_patches():
    note_colors = [
        ["~~"] * 9
        for note in NotesNames
    ]
    for piano_note in get_piano_notes():
        note_colors[piano_note.name.idx][piano_note.octave] = piano_note.get_rgb_patch()

    for i in range(len(note_colors)):
        note_colors[i] = [list(NotesNames)[i].value] + note_colors[i]

    note_colors = [[""] + [o for o in range(9)]] + note_colors

    t = tabulate.tabulate(note_colors, headers="firstrow", tablefmt="simple")
    return t


def get_piano_note_chord_color_patches():
    note_chord_colors = [
        [["~~"] * 3] * 3
        for _ in NotesNames
    ]
    for piano_note in get_piano_notes():
        if piano_note.octave not in {3, 4, 5}:
            continue
        chord_patches = [
            f"{chord_type.name:<11}" + ' '.join([_.get_rgb_patch() for _ in piano_note.get_chord(chord_type)])
            for chord_type in ChordTypes
        ]
        note_chord_colors[piano_note.name.idx][piano_note.octave - 3] = '\n'.join(chord_patches)

    for i in range(len(list(NotesNames))):
        note_chord_colors[i] = [list(NotesNames)[i].value] + note_chord_colors[i]

    note_colors = [[""] + [o for o in range(9)]] + note_chord_colors

    t = tabulate.tabulate(
        note_colors,
        headers="firstrow",
        tablefmt="rounded_grid"
    )
    return t


print(get_piano_note_color_patches())
print(get_piano_note_chord_color_patches())
