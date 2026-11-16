"""Background music player for the invitation."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.styles.theme import COLORS, FONTS, SHADOWS


def musica() -> rx.Component:
    """Render the invitation song and start playback when the page loads."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("music-2", size=28, color=COLORS["rose"], aria_hidden="true"),
                rx.audio(
                    src=rx.asset("Chiquita-Camilo-music.mp3"),
                    playing=True,
                    controls=True,
                    loop=True,
                    volume=0.65,
                    width="100%",
                    height="42px",
                ),
                spacing="3",
                align="center",
                width="100%",
                
            ),
        
            spacing="3",
            align="center",
            width="100%",
        ),
        width="100%",
        max_width="34rem",
        margin_x="auto",
        margin_y="1.5rem",
        padding="1.25rem",
        background_color=COLORS["white"],
        border=f"1px solid {COLORS['cream']}",
        border_radius="1.25rem",
        box_shadow=SHADOWS["soft"],
    )