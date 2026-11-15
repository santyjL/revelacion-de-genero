"""Invitation letter copy."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.components.ornaments import corners
from revelacion_de_genero.styles.style import BODY_TEXT
from revelacion_de_genero.styles.theme import FONTS, SPACE



def invitation() -> rx.Component:
    paragraphs = [
        "Agradecemos a Dios por este milagro que llena nuestro hogar de ilusión.",
        "Un corazón pequeñito crece dentro de mami y se alimenta del amor de papi.",
        "Con muchísimo amor y emoción queremos invitarte a compartir un momento muy especial con nosotros.",
    ]

    carta_bg = rx.asset("decorations/carta.png")

    return rx.box(
        corners(),
        rx.vstack(
            *[
                rx.text(
                    text,
                    style=BODY_TEXT,
                    font_size="1.16rem",
                    text_align="center",
                    line_height="1.65",
                    color="#46352C",
                )
                for text in paragraphs
            ],
            spacing="4",
            align="center",
            width="100%",
        ),
        class_name="invite-panel fade-up",
        margin_top=SPACE["md"],
        font_family=FONTS["body"],
        background_image=f"url('{carta_bg}')",
        background_size="full",
        background_position="center",
        background_repeat="no-repeat",
        width="100%",
        padding=["2rem 1.5rem", "3rem 3rem"],
        box_sizing="border-box",
    )

