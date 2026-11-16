"""The big reveal and team cards."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.components.ornaments import flourish
from revelacion_de_genero.state.rsvp_state import RsvpState
from revelacion_de_genero.styles.style import TEAM_BOY, TEAM_GIRL
from revelacion_de_genero.styles.theme import COLORS, FONTS, SPACE


def _reveal() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "¡Estamos a punto de descubrir si nuestro pequeño milagro será NIÑA o NIÑO!",
            as_="h2",
            font_size="clamp(1.55rem, 5.8vw, 2.15rem)",
            margin_top="0"
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
        align="center",
        width="100%",
    )


def _card(
    team: str,
    title: str,
    body: str,
    accent: str,
    style: dict,
    bear_image: str,
    bear_alt: str,
) -> rx.Component:
    is_selected = RsvpState.team == team
    return rx.box(rx.button(
        rx.vstack(
            rx.image(
                src=rx.asset(bear_image),
                alt=bear_alt,
                width="6.5rem",
                height="6.5rem",
                object_fit="contain",
            ),
            rx.heading(title, as_="h3", font_size="1.45rem", color=accent),
            rx.text(body, text_align="center", font_size="1.08rem", line_height="1.20"),
            spacing="3",
            align="center",
        ),
        style={
            **style,
            "border": rx.cond(is_selected, f"3px solid {COLORS['sepia']}", style["border"]),
            "box_shadow": rx.cond(is_selected, "0 0.6rem 1.4rem #46352c55", style["box_shadow"]),
        },
        class_name=rx.cond(
            is_selected,
            f"team-card team-card-{team} selected",
            f"team-card team-card-{team}",
        ),
        on_click=RsvpState.set_team(team),
        width="100%",
        min_height="18rem",
        height="6rem",
        white_space="normal",
        cursor="pointer",
        transition="transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease",
        _hover={"transform": "translateY(-0.2rem)", "box_shadow": "0 0.6rem 1.4rem #46352c33"},
    ),
        display="flex",
        direction="auto",
    )


def team_cards() -> rx.Component:
    return rx.vstack(
        _reveal(),
        rx.heading("¡Elige tu equipo!", as_="h2", font_size="clamp(1.6rem, 5.4vw, 2.1rem)", margin_top=SPACE["xs"]),
        rx.flex(
            _card(
                "boy",
                "TEAM NIÑO",
                "Si crees que será niño: Ven con una prenda en tono celeste y trae pañitos húmedos Huggies o Pampers.",
                COLORS["sepia"],
                TEAM_BOY,
                "decorations/oso-niño.png",
                "Osito vestido de celeste para el Team Niño",
            ),
            _card(
                "girl",
                      "TEAM NIÑA",
                "Si crees que será niña: Ven con una prenda en color rosado y trae pañales Huggies Natural care, Dermacare talla P, M, G o Pampers a partir de la talla 1.",
                COLORS["sepia"],
                TEAM_GIRL,
                "decorations/osita.png",
                "Osita con su pequeño osito para el Team Niña",
            ),
            direction=rx.breakpoints(initial="column", sm="row"),
            gap=SPACE["md"],
            width="100%",
        ),
        rx.text(
            "¡Elige tu equipo, ven preparado y acompáñanos a descubrir si acertaste!",
            font_family=FONTS["display"],
            font_style="italic",
            font_size="clamp(1.6rem, 7vw, 1.9rem)",
            text_align="center",
        ),
        class_name="invite-section fade-up",
        width="100%",
    )
