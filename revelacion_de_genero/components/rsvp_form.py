"""Attendance confirmation form."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.components.ornaments import corners, flourish
from revelacion_de_genero.state.rsvp_state import RsvpState
from revelacion_de_genero.styles.style import BUTTON, INPUT, LABEL, OPTION_CARD, PANEL
from revelacion_de_genero.styles.theme import COLORS


def _choice(value: str, label: str, selected: rx.Var, handler) -> rx.Component:
    return rx.box(
        rx.text(label),
        on_click=handler(value),
        style=OPTION_CARD,
        class_name=rx.cond(selected == value, "option-card selected", "option-card"),
        width="100%",
    )


def rsvp_form() -> rx.Component:
    return rx.box(
        corners(),
        rx.vstack(
            rx.heading("CONFIRMAR ASISTENCIA 🩷🩵", as_="h2", font_size="clamp(1.25rem, 5vw, 1.8rem)"),
            flourish(),
            rx.text("¡Queremos contar contigo en este día tan especial!"),
            rx.cond(
                RsvpState.submitted,
                rx.text(RsvpState.success_message, text_align="center", color=COLORS["sepia"]),
                rx.form(
                    rx.vstack(
                        rx.text("Tu nombre", style=LABEL),
                        rx.input(
                            id="guest-name",
                            name="guest_name",
                            placeholder="Escribe tu nombre",
                            value=RsvpState.guest_name,
                            on_change=RsvpState.set_guest_name,
                            style=INPUT,
                            max_length=100,
                            required=True,
                        ),
                        rx.text("¿Podrás asistir?", style=LABEL),
                        _choice("yes", "¡Sí, claro! ¡No me lo pierdo!", RsvpState.attendance, RsvpState.set_attendance),
                        _choice("no", "Esta vez no voy a poder.", RsvpState.attendance, RsvpState.set_attendance),
                        rx.text("Elige tu equipo (opcional)", style=LABEL),
                        _choice("boy", "TEAM NIÑO", RsvpState.team, RsvpState.set_team),
                        _choice("girl", "TEAM NIÑA", RsvpState.team, RsvpState.set_team),
                        _choice("unknown", "Aún no lo sé", RsvpState.team, RsvpState.set_team),
                        rx.cond(
                            RsvpState.error_message != "",
                            rx.text(RsvpState.error_message, color="#9a3b3b", font_size="0.92rem"),
                        ),
                        rx.button(
                            rx.cond(RsvpState.submitting, "Enviando…", "CONFIRMAR MI ASISTENCIA"),
                            type="submit",
                            style=BUTTON,
                            class_name="cta-button",
                            disabled=RsvpState.submitting,
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    on_submit=RsvpState.submit,
                    width="100%",
                ),
            ),
            spacing="4",
            align="center",
            width="100%",
        ),
        style=PANEL,
        class_name="invite-panel fade-up",
        width="100%",
        margin_top="2rem",
    )
