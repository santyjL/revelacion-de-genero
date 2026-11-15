"""Event date, time and place."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.components.ornaments import corners, flourish
from revelacion_de_genero.config.settings import settings
from revelacion_de_genero.styles.style import LABEL, PANEL
from revelacion_de_genero.styles.theme import COLORS, FONTS, SPACE

MONTHS_ES = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}


def _detail(icon: str, label: str, value: str) -> rx.Component:
    return rx.hstack(
        rx.text(icon, font_size="1.25rem", aria_hidden="true"),
        rx.vstack(
            rx.text(label, style=LABEL, font_size="0.72rem"),
            rx.text(value, font_family=FONTS["serif"], font_size="1.3rem", color=COLORS["sepia"]),
            spacing="1",
            align="start",
        ),
        spacing="3",
        align="center",
        width="100%",
        justify="start",
    )


def event_details() -> rx.Component:
    event_date = settings.event_date
    pretty_date = f"{event_date.day} de {MONTHS_ES[event_date.month]} de {event_date.year}"
    hour = settings.event_time.strftime("%-I:%M %p").replace("AM", "AM").replace("PM", "PM")
    hour_display = "3:00 PM" if settings.event_time.hour == 15 else hour
    return rx.box(
        corners(),
        rx.vstack(
            rx.heading("Los detalles", as_="h2", font_size="clamp(1.6rem, 5.4vw, 2.1rem)"),
            flourish(),
            _detail("📅", "Fecha", pretty_date),
            _detail("🕒", "Hora", hour_display),
            _detail("📍", "Lugar", settings.event_place),
            spacing="4",
            align="start",
            width="100%",
        ),
        style=PANEL,
        class_name="invite-panel fade-up",
        width="100%",
        margin_top=SPACE["lg"],
    )
