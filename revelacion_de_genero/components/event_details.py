"""Event date, time and place."""

from __future__ import annotations

from datetime import timedelta
from urllib.parse import urlencode

import reflex as rx

from revelacion_de_genero.config.settings import settings
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


def _detail_card(
    icon: str,
    label: str,
    value: str,
    link_text: str,
    href: str,
    accent: str,
    secondary_value: str = "",
) -> rx.Component:
    content = [
        rx.icon(icon, size=96, stroke_width=1.35, color=accent, aria_hidden="true"),
        rx.text(
            label,
            font_family=FONTS["sans"],
            font_size="1rem",
            font_weight="700",
            letter_spacing="0.12em",
            text_transform="uppercase",
            color=COLORS["brown"],
        ),
        rx.text(
            value,
            font_family=FONTS["serif"],
            font_size="clamp(1.65rem, 6vw, 2.2rem)",
            font_weight="600",
            line_height="1.25",
            color=COLORS["sepia"],
            text_align="center",
        ),
    ]
    if secondary_value:
        content.append(
            rx.text(
                secondary_value,
                font_family=FONTS["serif"],
                font_size="1.65rem",
                font_weight="600",
                color=COLORS["sepia"],
            )
        )
    content.append(
        rx.link(
            rx.hstack(
                rx.text(link_text),
                rx.icon("arrow-up-right", size=20, aria_hidden="true"),
                spacing="2",
                align="center",
            ),
            href=href,
            target="_blank",
            rel="noopener noreferrer",
            color=COLORS["brown"],
            font_family=FONTS["sans"],
            font_size="1.05rem",
            font_weight="700",
            text_decoration="underline",
            text_underline_offset="0.25em",
            text_align="center",
            _hover={"color": accent},
        )
    )

    return rx.box(
        rx.vstack(
            *content,
            spacing="3",
            align="center",
            justify="center",
            width="100%",
        ),
        width="100%",
        min_height="20rem",
        padding="clamp(1.5rem, 6vw, 2.5rem)",
        display="flex",
        align_items="center",
        justify_content="center",
        background_color=COLORS["white"],
        background_image=f"linear-gradient(155deg, {COLORS['white']} 15%, {COLORS['paper']} 100%)",
        border_top=f"5px solid {accent}",
        border_radius="1.5rem",
        box_shadow="0 1rem 2.5rem rgba(70, 53, 44, 0.09)",
        transition="transform 180ms ease, box-shadow 180ms ease",
        _hover={
            "transform": "translateY(-0.2rem)",
            "box_shadow": "0 1.25rem 3rem rgba(70, 53, 44, 0.14)",
        },
    )


def event_details() -> rx.Component:
    event_date = settings.event_date
    pretty_date = f"{event_date.day} de {MONTHS_ES[event_date.month]} de {event_date.year}"
    hour = settings.event_time.strftime("%-I:%M %p")
    start = settings.event_datetime
    end = start + timedelta(hours=2)
    calendar_url = "https://calendar.google.com/calendar/render?" + urlencode(
        {
            "action": "TEMPLATE",
            "text": "Revelación de género",
            "dates": f"{start:%Y%m%dT%H%M%S}/{end:%Y%m%dT%H%M%S}",
            "ctz": settings.timezone_name,
            "location": settings.event_place,
        }
    )
    location_url = "https://www.google.com/maps/place/Pikitos+Restaurante+Nica-Mex/@12.1175692,-86.2829372,15z/data=!4m10!1m2!2m1!1spikitos!3m6!1s0x8f7155c6daddbc63:0xe8f56a52297c142d!8m2!3d12.1175692!4d-86.2649128!15sCgdwaWtpdG9zWgkiB3Bpa2l0b3OSARJtZXhpY2FuX3Jlc3RhdXJhbnTgAQA!16s%2Fg%2F11t9kymqy1?entry=ttu&g_ep=EgoyMDI2MTExMC4wIKXMDSoASAFQAw%3D%3D" + urlencode(
        {"api": "1", "query": settings.event_place}
    )

    return rx.vstack(
        rx.vstack(
            _detail_card(
                "calendar-days",
                "Fecha y hora",
                pretty_date,
                "Agendar en Google Calendar",
                calendar_url,
                COLORS["gold"],
                secondary_value=hour,
            ),
            _detail_card(
                "map-pin",
                "Lugar",
                settings.event_place,
                "Ver ubicación en Google Maps",
                location_url,
                COLORS["rose"],
            ),
            spacing="5",
            align="stretch",
            width="100%",
        ),
        spacing="5",
        align="center",
        width="100%",
        background_color="#00000000",
        border_top=f"1px solid {COLORS['cream']}",
        class_name="invite-panel fade-up",
        margin_top=SPACE["lg"],
    )
