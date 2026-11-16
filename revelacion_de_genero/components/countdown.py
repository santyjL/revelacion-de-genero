"""Client-side countdown synchronized to America/Managua."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.components.ornaments import flourish
from revelacion_de_genero.config.settings import settings
from revelacion_de_genero.styles.style import COUNT_CELL
from revelacion_de_genero.styles.theme import COLORS, FONTS, SPACE


def _unit(key: str, label: str) -> rx.Component:
    return rx.box(
        rx.text(
            "00",
            custom_attrs={"data-unit": key},
            font_family=FONTS["serif"],
            font_size="clamp(1.8rem, 5vw, 2.1rem)",
            color=COLORS["sepia"],
            class_name="pulse-soft",
        ),
        rx.text(
            label,
            font_family=FONTS["sans"],
            font_size="0.8rem",
            letter_spacing="0.12em",
            text_transform="uppercase",
            color=COLORS["brown"],
        ),
        style=COUNT_CELL,
        class_name="count-cell",
        text_align="center",
    )


def countdown() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "¡ACTIVA LA CUENTA REGRESIVA Y PREPÁRATE PARA LA SORPRESA!",
            as_="h2",
            font_size="clamp(1.45rem, 5vw, 2rem)",
        ),
        flourish(),
        rx.box(
            rx.flex(
                _unit("days", "Días"),
                _unit("hours", "Horas"),
                _unit("minutes", "Minutos"),
                _unit("seconds", "Segundos"),
                gap="0.55rem",
                width="100%",
                custom_attrs={"data-countdown-live": "true"},
            ),
            
            id="event-countdown",
            custom_attrs={"data-deadline-ms": str(settings.event_deadline_ms)},
            width="100%",
        ),
        rx.script(src="/countdown.js"),
        class_name="invite-section fade-up",
        margin=0,
        width="100%",
    )
