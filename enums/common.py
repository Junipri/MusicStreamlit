from __future__ import annotations

from enum import Enum


class Selectable(Enum):
    pass


class _Radioable(Enum):
    @property
    def value_label(self) -> str:
        return str(self.value)

    @property
    def name_label(self) -> str:
        return str(self.name.capitalize())

    @classmethod
    def radio_format_func(cls, item: Enum, use_value: bool = True) -> str:
        if use_value:
            return str(item.value)
        else:
            return item.name.capitalize()

    @classmethod
    def get_radio_session_state_var(cls) -> str:
        return f"SELECTED_{cls.__name__}Enum"

    @classmethod
    def radio(cls, label=None):
        import streamlit as st
        label = label or f"{cls.__name__}:"

        st.radio(
            label=label,
            options=list(cls),
            format_func=cls.radio_format_func,
            key=cls.get_radio_session_state_var(),
            horizontal=True
        )

    @classmethod
    def get_radio(cls) -> _Radioable:
        import streamlit as st
        key: str = cls.get_radio_session_state_var()

        if key not in st.session_state:
            st.session_state[key] = None

        return st.session_state[key]


class Octaves(_Radioable):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
