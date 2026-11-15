"""Invitation letter copy."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.components.ornaments import corners
from revelacion_de_genero.styles.style import BODY_TEXT, PANEL
from revelacion_de_genero.styles.theme import FONTS, SPACE


def invitation() -> rx.Component:
    paragraphs = [
        "Agradecemos a Dios por este milagro que llena nuestro hogar de ilusión.",
        "Un corazón pequeñito crece dentro de mami y se alimenta del amor de papi.",
        "Con muchísimo amor y emoción queremos invitarte a compartir un momento muy especial con nosotros.",
    ]
    return rx.box(
        corners(),
        rx.vstack(
            *[
                rx.text(text, style=BODY_TEXT, font_size="1.05rem", text_align="center")
                for text in paragraphs
            ],
            spacing="4",
            align="center",
        ),
        style=PANEL,
        class_name="invite-panel fade-up",
        margin_top=SPACE["md"],
        font_family=FONTS["body"],
        width="100%",
    )
