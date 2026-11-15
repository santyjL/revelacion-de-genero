"""Single-page vintage invitation."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.components.baby_photo import baby_photo
from revelacion_de_genero.components.countdown import countdown
from revelacion_de_genero.components.event_details import event_details
from revelacion_de_genero.components.footer import footer
from revelacion_de_genero.components.hero import hero
from revelacion_de_genero.components.invitation import invitation
from revelacion_de_genero.components.rsvp_form import rsvp_form
from revelacion_de_genero.components.team_cards import team_cards
from revelacion_de_genero.styles.style import PAGE, SHELL


def home_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            hero(),
            invitation(),
            baby_photo(),
            team_cards(),
            event_details(),
            countdown(),
            rsvp_form(),
            footer(),
            spacing="0",
            width="100%",
            align="center",
        ),
        style={**PAGE, **SHELL},
        class_name="invite-shell",
    )
