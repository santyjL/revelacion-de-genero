"""Baby photograph and configurable Bible verse."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.components.ornaments import flourish, tiny_icon
from revelacion_de_genero.config.settings import settings
from revelacion_de_genero.styles.style import PHOTO_FRAME
from revelacion_de_genero.styles.theme import COLORS, FONTS, SPACE


def _photo() -> rx.Component:
    if settings.ultrasound_video_src:
        return rx.el.video(
            src=settings.ultrasound_video_src,
            controls=True,
            auto_play=True,
            muted=True,
            loop=True,
            plays_inline=True,
            preload="metadata",
            class_name="ultrasound-video",
            aria_label="Ultrasonido de nuestro pequeño milagro",
        )
    if settings.baby_photo_src:
        return rx.image(
            src=settings.baby_photo_src,
            alt="Fotografía del bebé en camino",
            class_name="photo-inner",
            width="100%",
            height="auto",
        )
    return rx.box(
        rx.text("Nuestro milagro"),
        class_name="placeholder-photo",
        role="img",
        aria_label="Fotografía por confirmar",
    )


def _verse() -> rx.Component:
    if settings.bible_verse_text and settings.bible_verse_reference:
        return rx.vstack(
            rx.text(
                settings.bible_verse_text,
                font_family=FONTS["display"],
                font_style="italic",
                color=COLORS["sepia"],
                text_align="center",
            ),
            rx.text(
                settings.bible_verse_reference,
                font_family=FONTS["sans"],
                font_size="0.85rem",
                letter_spacing="0.08em",
                color=COLORS["gold"],
            ),
            spacing="2",
            align="center",
        )
    return rx.text(
        "Versículo por confirmar",
        font_family=FONTS["script"],
        font_size="1.4rem",
        color=COLORS["gold"],
    )


def baby_photo() -> rx.Component:
    return rx.vstack(
        tiny_icon("🎀"),
        rx.heading("Nuestro pequeño milagro", as_="h2", font_size="clamp(1.6rem, 5.5vw, 2.2rem)"),
        flourish(),
        rx.box(_photo(), style=PHOTO_FRAME, class_name="photo-frame float-soft"),
        _verse(),
        class_name="invite-section fade-up",
        width="100%",
    )
