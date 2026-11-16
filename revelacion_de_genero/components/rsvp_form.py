"""Attendance confirmation form."""

from __future__ import annotations

import reflex as rx

from revelacion_de_genero.components.ornaments import corners, flourish
from revelacion_de_genero.state.rsvp_state import RsvpState
from revelacion_de_genero.styles.style import BUTTON, INPUT, LABEL, OPTION_CARD, PANEL
from revelacion_de_genero.styles.theme import COLORS, SHADOWS


def _choice(
    value: str,
    label: str,
    selected: rx.Var,
    handler,
    width: str = "50px",
    height: str = "3rem",
) -> rx.Component:
    is_selected = selected == value
    return rx.button(
        rx.text(label, text_align="center", line_height="0.9"),
        type="button",
        on_click=handler(value),
        style={
            **OPTION_CARD,
            "height": height,
            "text_align": "center",
            "white_space": "normal",
            "border": rx.cond(is_selected, f"2px solid {COLORS['sepia']}", OPTION_CARD["border"]),
            "background_color": rx.cond(
                is_selected,
                COLORS["cream"],
                OPTION_CARD["background_color"],
            ),
            "box_shadow": rx.cond(is_selected, SHADOWS["soft"], "none"),
        },
        class_name=rx.cond(is_selected, "option-card selected", "option-card"),
        width=width,
        margin=0,
        padding=0
    )


def _family_name_input(
    index: int,
    value: rx.Var,
    on_change,
) -> rx.Component:
    return rx.vstack(
        rx.text(f"Nombre del integrante {index}", style=LABEL),
        rx.input(
            id=f"family-member-{index}",
            name=f"family_member_{index}",
            placeholder=f"Nombre del integrante {index}",
            value=value,
            on_change=on_change,
            style=INPUT,
            max_length=100,
            required=True,
        ),
        width="100%",
        spacing="2",
    )


def rsvp_form() -> rx.Component:
    return rx.box(
        corners(),
        rx.vstack(
            rx.heading("CONFIRMAR ASISTENCIA", as_="h2", font_size="clamp(1.25rem, 5vw, 1.8rem)"),
            flourish(),
            rx.text("¡Queremos contar contigo en este día tan especial!"),
            rx.cond(
                RsvpState.submitted,
                rx.vstack(
                    rx.text(
                        RsvpState.success_message,
                        text_align="center",
                        color=COLORS["sepia"],
                    ),
                    rx.cond(
                        RsvpState.notification_message != "",
                        rx.text(
                            RsvpState.notification_message,
                            text_align="center",
                            color=COLORS["brown"],
                            font_size="0.95rem",
                        ),
                        rx.fragment(),
                    ),
                    width="100%",
                    spacing="2",
                    align="center",
                ),
                rx.form(
                    rx.vstack(
                        rx.text("¿Podrás asistir?", style=LABEL, text_align="center"),
                        rx.box(
                            _choice(
                                "yes",
                                "Sí asistiré",
                                RsvpState.attendance,
                                RsvpState.set_attendance,
                            ),
                            _choice(
                                "no",
                                "No asistiré",
                                RsvpState.attendance,
                                RsvpState.set_attendance,
                            ),
                            width="50%",
                            spacing="2",
                            gap="0.5rem",
                            align_items="center",
                            justify="center",
                            display="flex",
                            direction="row",

                        ),
                        rx.text("Tipo de invitación", style=LABEL),
                        rx.box(
                            _choice(
                                "individual",
                                "Individual",
                                RsvpState.invitation_type,
                                RsvpState.set_invitation_type,

                            ),
                            _choice(
                                "family",
                                "Familiar",
                                RsvpState.invitation_type,
                                RsvpState.set_invitation_type,
                            ),
                            width="50%",
                            spacing="3",
                            gap="0.5rem",
                            align="stretch",
                            justify="center",
                            display="flex",
                            direction="row",
                           ),
                        rx.text(
                            rx.cond(
                                RsvpState.invitation_type == "family",
                                "Cabeza de familia",
                                "Tu nombre",
                            ),
                            style=LABEL,
                        ),
                        rx.input(
                            id="guest-name",
                            name="guest_name",
                            placeholder=rx.cond(
                                RsvpState.invitation_type == "family",
                                "Tu nombre",
                                "Escribe tu nombre",
                            ),
                            value=RsvpState.guest_name,
                            on_change=RsvpState.set_guest_name,
                            style=INPUT,
                            max_length=100,
                            required=True,
                        ),
                        rx.cond(
                            RsvpState.invitation_type == "family",
                                rx.vstack(
                                    rx.text(
                                        "Cantidad de integrantes (incluyéndote)",
                                        style=LABEL,
                                        ),
                                    rx.input(
                                        id="family-count",
                                        name="family_count",
                                        type="number",
                                        min="2",
                                        max="6",
                                        value=RsvpState.family_count,
                                        on_change=RsvpState.set_family_count,
                                        style=INPUT,
                                        required=True,
                                        ),
                                    _family_name_input(
                                        2,
                                        RsvpState.family_member_2,
                                        RsvpState.set_family_member_2,
                                        ),
                                        rx.cond(
                                            RsvpState.family_count >= 3,
                                            _family_name_input(
                                                3,
                                                RsvpState.family_member_3,
                                                RsvpState.set_family_member_3,
                                            ),
                                        ),
                                        rx.cond(
                                            RsvpState.family_count >= 4,
                                            _family_name_input(
                                                4,
                                                RsvpState.family_member_4,
                                                RsvpState.set_family_member_4,
                                            ),
                                        ),
                                        rx.cond(
                                            RsvpState.family_count >= 5,
                                            _family_name_input(
                                                5,
                                                RsvpState.family_member_5,
                                                RsvpState.set_family_member_5,
                                            ),
                                        ),
                                        rx.cond(
                                            RsvpState.family_count >= 6,
                                            _family_name_input(
                                                6,
                                                RsvpState.family_member_6,
                                                RsvpState.set_family_member_6,
                                            ),
                                        ),
                                        width="100%",
                                        spacing="3",
                                    ),
                                ),
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
