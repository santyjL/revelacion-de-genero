"""RSVP form state. Coordinates validation and CSV persistence."""

from __future__ import annotations

from datetime import datetime

import reflex as rx

from revelacion_de_genero.config.settings import settings
from revelacion_de_genero.services.csv_service import recent_duplicate, save_attendance
from revelacion_de_genero.services.validation_service import validate_rsvp

YES_MESSAGE = "¡Qué alegría! Te esperamos para descubrir juntos la sorpresa."
NO_MESSAGE = "Gracias por avisarnos. Te tendremos presente con mucho cariño."


class RsvpState(rx.State):
    """Visitor RSVP interaction."""

    guest_name: str = ""
    attendance: str = ""
    team: str = "unknown"
    error_message: str = ""
    success_message: str = ""
    submitting: bool = False
    submitted: bool = False

    @rx.event
    def set_guest_name(self, value: str):
        self.guest_name = value
        self.error_message = ""

    @rx.event
    def set_attendance(self, value: str):
        self.attendance = value
        self.error_message = ""

    @rx.event
    def set_team(self, value: str):
        self.team = value
        self.error_message = ""

    @rx.event
    def submit(self, form_data: dict | None = None):
        if self.submitting or self.submitted:
            return
        self.submitting = True
        self.error_message = ""
        payload = form_data or {}
        name = str(payload.get("guest_name") or self.guest_name)
        result = validate_rsvp(name, self.attendance, self.team)
        if not result.ok:
            self.error_message = result.message
            self.submitting = False
            return
        if recent_duplicate(result.name, settings.rsvp_min_seconds):
            self.error_message = "Ya recibimos tu confirmación. ¡Gracias!"
            self.submitting = False
            return
        saved = save_attendance(
            {
                "name": result.name,
                "attendance": result.attendance,
                "team": result.team,
                "submitted_at": datetime.now(settings.timezone).isoformat(),
            }
        )
        if not saved:
            self.error_message = "No pudimos guardar tu respuesta. Inténtalo de nuevo."
            self.submitting = False
            return
        self.success_message = YES_MESSAGE if result.attendance == "yes" else NO_MESSAGE
        self.submitted = True
        self.guest_name = ""
        self.attendance = ""
        self.team = "unknown"
        self.submitting = False
