from enum import Enum
from functools import wraps

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


class TextEffects(Enum):
    _RESET = "0"

    BOLD = "1"
    DIM = "2"
    ITALIC = "3"
    UNDERLINE = "4"
    BLINK = "5"
    REVERSE = "7"
    HIDDEN = "8"
    STRIKETHROUGH = "9"

    def __str__(self):
        return f"\033[{self.value}m"

    def apply(self, text: str) -> str:
        return f"{self}{text}{TextEffects._RESET}"


def color_text(text: str, rgb: tuple[int, ...]):
    r, g, b = rgb
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


class TextColors(Enum):
    _RESET = "0"

    BLACK = "30"
    RED = "31"
    GREEN = "32"
    YELLOW = "33"
    BLUE = "34"
    MAGENTA = "35"
    CYAN = "36"
    WHITE = "37"

    BRIGHT_BLACK = "90"
    BRIGHT_RED = "91"
    BRIGHT_GREEN = "92"
    BRIGHT_YELLOW = "93"
    BRIGHT_BLUE = "94"
    BRIGHT_MAGENTA = "95"
    BRIGHT_CYAN = "96"
    BRIGHT_WHITE = "97"

    def __str__(self):
        return f"\033[{self.value}m"

    def apply(self, text: str) -> str:
        return f"{self}{text}{TextColors._RESET}"


def cache_to_disk(cache_dir='.cache'):
    import hashlib
    import os
    import pickle

    os.makedirs(cache_dir, exist_ok=True)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate file name
            key = pickle.dumps((func.__name__, args, kwargs))
            key_hash = hashlib.md5(key).hexdigest()
            cache_file = os.path.join(cache_dir, f"{func.__name__}_{key_hash}.pkl")

            # Check cache
            if os.path.exists(cache_file):
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)

            # Run function
            result = func(*args, **kwargs)

            # Cache to disk
            with open(cache_file, 'wb') as f:
                pickle.dump(result, f)
            return result

        return wrapper

    return decorator


def adsr_envelope(
        audio_signal,
        attack_percent: float,
        decay_percent: float,
        sustain_amplitude: float,
        release_percent: float,
        sr: int = 44100
):
    num_samples: int = audio_signal.shape[0]

    attack_samples = int(attack_percent * num_samples)
    decay_samples = int(decay_percent * num_samples)
    release_samples = int(release_percent * num_samples)
    sustain_samples = int(num_samples - attack_samples - decay_samples - release_samples)

    # Create envelope segments
    attack_env = np.linspace(0, 1, attack_samples)  # Attack: ramp from 0 to 1
    decay_env = np.linspace(1, sustain_amplitude, decay_samples)  # Decay: ramp from 1 to sustain_level
    sustain_env = np.full(sustain_samples, sustain_amplitude)  # Sustain: constant sustain_level
    release_env = np.linspace(sustain_amplitude, 0, release_samples)

    adsr_env = np.concatenate([attack_env, decay_env, sustain_env, release_env])

    duration_in_seconds = num_samples / sr
    t = np.linspace(0, duration_in_seconds, int(duration_in_seconds * sr), endpoint=False)

    enveloped_audio = adsr_env

    fig, ax = plt.subplots()
    ax.plot(t, audio_signal)
    # ax.plot(t, enveloped_audio)
    # ax.plot(t, adsr_env)
    st.pyplot(fig)

    return enveloped_audio
