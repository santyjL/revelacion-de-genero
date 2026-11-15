"""The big reveal and team cards."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.components.ornaments import flourish
from revelacion_de_genero.styles.style import TEAM_BOY, TEAM_GIRL
from revelacion_de_genero.styles.theme import COLORS, FONTS, SPACE


def _reveal() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "¡Estamos a punto de descubrir si nuestro pequeño milagro será NIÑA o NIÑO!",
            as_="h2",
            font_size="clamp(1.25rem, 5.4vw, 1.85rem)",
        ),
        flourish(),
        rx.text("Un día lleno de alegría, amor y mucha ilusión nos espera."),
        rx.text(
            "¿NOS ACOMPAÑAS A DESCUBRIRLO?",
            font_family=FONTS["serif"],
            font_weight="700",
            letter_spacing="0.06em",
            color=COLORS["sepia"],
            margin_top="0.75rem",
        ),
        spacing="3",
        align="center",
        width="100%",
    )


def _card(title: str, body: str, accent: str, style: dict, emoji: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(emoji, font_size="1.8rem"),
            rx.heading(title, as_="h3", font_size="1.2rem", color=accent),
            rx.text(body, text_align="center", font_size="0.98rem"),
            spacing="3",
            align="center",
        ),
        style=style,
        width="100%",
        min_height="14rem",
    )


def team_cards() -> rx.Component:
    return rx.vstack(
        _reveal(),
        rx.heading("¡Elige tu equipo!", as_="h2", font_size="clamp(1.3rem, 5vw, 1.8rem)", margin_top=SPACE["lg"]),
        rx.flex(
            _card(
                "TEAM NIÑO",
                "Si crees que será niño: Ven con una prenda en tono celeste y trae pañitos húmedos.",
                COLORS["sepia"],
                TEAM_BOY,
                "🧸🩵",
            ),
            _card(
                "TEAM NIÑA",
                "Si crees que será niña: Ven con una prenda en tono rosado y trae pañales Huggies Dermacare o Pampers talla P, M o G en adelante.",
                COLORS["sepia"],
                TEAM_GIRL,
                "🧸🩷",
            ),
            direction=rx.breakpoints(initial="column", sm="row"),
            gap=SPACE["md"],
            width="100%",
        ),
        rx.text(
            "¡Elige tu equipo, ven preparado y acompáñanos a descubrir si acertaste!",
            font_family=FONTS["display"],
            font_style="italic",
            text_align="center",
        ),
        class_name="invite-section fade-up",
        width="100%",
    )
