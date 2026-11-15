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
            font_size="clamp(1.15rem, 4.8vw, 1.7rem)",
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
            rx.center(
                rx.text(
                    "¡Llegó el gran día! La sorpresa está por revelarse.",
                    font_family=FONTS["script"],
                    font_size="clamp(1.4rem, 5vw, 2rem)",
                    color=COLORS["gold"],
                    text_align="center",
                ),
                custom_attrs={"data-countdown-done": "true"},
                display="none",
                width="100%",
                min_height="6rem",
            ),
            id="event-countdown",
            custom_attrs={"data-deadline-ms": str(settings.event_deadline_ms)},
            width="100%",
        ),
        rx.script(src="/countdown.js"),
        class_name="invite-section fade-up",
        spacing="4",
        width="100%",
    )
