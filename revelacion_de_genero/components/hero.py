"""Hero announcement."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.components.ornaments import flourish, tiny_icon
from revelacion_de_genero.styles.style import HEADING
from revelacion_de_genero.styles.theme import COLORS, FONTS, SPACE


def hero() -> rx.Component:
    return rx.vstack(
        tiny_icon("🧸"),
        rx.heading(
            "¡UNA GRAN SORPRESA ESTÁ POR LLEGAR! 🧸🩷🩵",
            as_="h1",
            font_size="clamp(1.55rem, 7.2vw, 2.7rem)",
            style=HEADING,
        ),
        flourish(),
        rx.text(
            "Una invitación de familia",
            class_name="script-text",
            font_size="clamp(1.45rem, 5vw, 2rem)",
            font_family=FONTS["script"],
            color=COLORS["gold"],
        ),
        class_name="invite-section fade-up",
        padding_top=SPACE["xl"],
        width="100%",
    )
