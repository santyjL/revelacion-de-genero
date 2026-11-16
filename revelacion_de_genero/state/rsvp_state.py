"""RSVP form state. Coordinates validation and CSV persistence."""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4

import reflex as rx

from revelacion_de_genero.config.settings import settings
from revelacion_de_genero.services.csv_service import recent_duplicate, save_attendance_batch
from revelacion_de_genero.services.email_service import send_rsvp_notification
from revelacion_de_genero.services.validation_service import validate_rsvp

YES_MESSAGE = "¡Qué alegría! Te esperamos para descubrir juntos la sorpresa."
NO_MESSAGE = "Gracias por avisarnos. Te tendremos presente con mucho cariño."


class RsvpState(rx.State):
    """Visitor RSVP interaction."""

    guest_name: str = ""
    family_member_2: str = ""
    family_member_3: str = ""
    family_member_4: str = ""
    family_member_5: str = ""
    family_member_6: str = ""
    family_count: int = 2
    invitation_type: str = "individual"
    attendance: str = ""
    team: str = ""
    error_message: str = ""
    success_message: str = ""
    notification_message: str = ""
    submitting: bool = False
    submitted: bool = False

    @rx.event
    def set_guest_name(self, value: str):
        self.guest_name = value
        self.error_message = ""

    @rx.event
    def set_family_member_2(self, value: str):
        self.family_member_2 = value

    @rx.event
    def set_family_member_3(self, value: str):
        self.family_member_3 = value

    @rx.event
    def set_family_member_4(self, value: str):
        self.family_member_4 = value

    @rx.event
    def set_family_member_5(self, value: str):
        self.family_member_5 = value

    @rx.event
    def set_family_member_6(self, value: str):
        self.family_member_6 = value

    @rx.event
    def set_family_count(self, value: str):
        try:
            self.family_count = int(value)
        except ValueError:
            self.error_message = "La invitación familiar debe incluir entre 2 y 6 integrantes."
            return
        self.error_message = ""

    @rx.event
    def set_invitation_type(self, value: str):
        if value in {"individual", "family"}:
            self.invitation_type = value
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
        if self.invitation_type not in {"individual", "family"}:
            self.error_message = "Selecciona el tipo de invitación."
            self.submitting = False
            return
        if self.invitation_type == "family" and not 2 <= self.family_count <= 6:
            self.error_message = "La invitación familiar debe incluir entre 2 y 6 integrantes."
            self.submitting = False
            return
        member_fields = [
            ("guest_name", self.guest_name),
            ("family_member_2", self.family_member_2),
            ("family_member_3", self.family_member_3),
            ("family_member_4", self.family_member_4),
            ("family_member_5", self.family_member_5),
            ("family_member_6", self.family_member_6),
        ]
        member_limit = self.family_count if self.invitation_type == "family" else 1
        names = [
            str(payload.get(field_name, state_value) or "")
            for field_name, state_value in member_fields[:member_limit]
        ]
        results = [
            validate_rsvp(name, self.attendance, self.team)
            for name in names
        ]
        invalid_result = next((result for result in results if not result.ok), None)
        if invalid_result is not None:
            self.error_message = invalid_result.message
            self.submitting = False
            return
        if any(recent_duplicate(result.name, settings.rsvp_min_seconds) for result in results):
            self.error_message = "Ya recibimos una confirmación reciente con uno de esos nombres."
            self.submitting = False
            return
        submitted_at = datetime.now(settings.timezone).isoformat()
        invitation_id = uuid4().hex
        records = [
            {
                "invitation_id": invitation_id,
                "invitation_type": self.invitation_type,
                "name": result.name,
                "attendance": result.attendance,
                "team": result.team,
                "submitted_at": submitted_at,
            }
            for result in results
        ]
        saved = save_attendance_batch(records)
        if not saved:
            self.error_message = "No pudimos guardar tu respuesta. Inténtalo de nuevo."
            self.submitting = False
            return
        self.success_message = YES_MESSAGE if results[0].attendance == "yes" else NO_MESSAGE
        self.notification_message = "Enviando aviso a los organizadores..."
        self.submitted = True
        self.guest_name = ""
        self.family_member_2 = ""
        self.family_member_3 = ""
        self.family_member_4 = ""
        self.family_member_5 = ""
        self.family_member_6 = ""
        self.family_count = 2
        self.invitation_type = "individual"
        self.attendance = ""
        self.submitting = False
        return RsvpState.send_confirmation_notification(records)

    @rx.event(background=True)
    async def send_confirmation_notification(self, records: list[dict[str, str]]):
        """Send an RSVP notification without blocking the form."""
        result = await asyncio.to_thread(send_rsvp_notification, records)
        async with self:
            if result["sent"]:
                self.notification_message = "Aviso enviado a los organizadores."
            else:
                self.notification_message = (
                    "Tu respuesta quedó guardada, pero no se pudo enviar el aviso a los "
                    "organizadores. Por favor, avísales directamente."
                )
