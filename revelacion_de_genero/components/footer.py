"""Closing signature."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.components.ornaments import flourish
from revelacion_de_genero.styles.theme import COLORS, FONTS, SPACE


def footer() -> rx.Component:
    return rx.vstack(
        flourish(),
        rx.text("Con cariño,", font_family=FONTS["script"], font_size="1.8rem", color=COLORS["gold"]),
        rx.text("Los futuros papás. 🤍", font_family=FONTS["serif"], color=COLORS["sepia"]),
        rx.text("—", color=COLORS["gold"]),
        class_name="invite-section fade-up",
        padding_bottom=SPACE["xl"],
        width="100%",
    )
