import colorsys
from enum import Enum, auto

import numpy as np
import tabulate

from enums.notes import NotesNames, get_piano_notes
from utils.common import color_text


class Colors(Enum):
    RED = auto()
    ORANGE = auto()
    YELLOW = auto()

    BLUE = auto()


class PrimaryColors(Enum):
    RED = "RED"
    YELLOW = "YELLOW"
    BLUE = "BLUE"


class SecondaryColors(Enum):
    GREEN = "GREEN"
    ORANGE = "ORANGE"
    PURPLE = "PURPLE"


class TertiaryColors(Enum):
    YELLOW_ORANGE = "YELLOW_ORANGE"
    RED_ORANGE = "RED_ORANGE"
    BLUE_PURPLE = "BLUE_PURPLE"
    BLUE_GREEN = "BLUE_GREEN"
    YELLOW_GREEN = "YELLOW_GREEN"



note_colors = [
    [""] * 9
    for note in NotesNames
]

for piano_note in get_piano_notes():
    note_colors[piano_note.name.idx][piano_note.octave] = color_text(
        "▒▒",
        tuple(
            int(_ * 255)
            for _ in colorsys.hls_to_rgb(
                piano_note.name.hue,
                octave_to_lightness(
                    octave=piano_note.octave,
                    l_clamp=(0.1, 0.9)
                ),
                1.0
            )
        )
    )

for i in range(len(note_colors)):
    note_colors[i] = [list(NotesNames)[i].value] + note_colors[i]

note_colors = [[""] + [o for o in range(9)]] + note_colors

print(tabulate.tabulate(note_colors, headers="firstrow", tablefmt="simple"))
