"""Hero announcement."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.components.ornaments import flourish
from revelacion_de_genero.styles.style import HEADING
from revelacion_de_genero.styles.theme import COLORS, FONTS, SPACE


def hero() -> rx.Component:
    return rx.vstack(
        rx.image(
            src=rx.asset("decorations/parejita-de-osos.png"),
            alt="Osita y osito celebrando juntos",
            width="clamp(10rem, 35vw, 12rem)",
            height="auto",
            class_name="float-soft",
        ),
        rx.heading(
            "¡UNA GRAN SORPRESA ESTÁ POR LLEGAR!",
            as_="h1",
            font_size="clamp(1.9rem, 7.5vw, 3.1rem)",
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
