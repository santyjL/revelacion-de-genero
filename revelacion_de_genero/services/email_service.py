"""Gmail API delivery for the daily attendance report."""

from __future__ import annotations

import base64
import json
import logging
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from typing import Any

from revelacion_de_genero.config.settings import settings
from revelacion_de_genero.services.csv_service import count_attendance, export_attendance

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
SUBJECT = "Gender Reveal - Reporte diario de confirmaciones"
BODY = """Hola,

Adjunto encontrarás el reporte actualizado de confirmaciones
de asistencia para la revelación de género del 29 de noviembre.

El archivo contiene los registros recibidos hasta el momento.

Saludos.
"""


def _load_log(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _write_log(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def already_sent(day_key: str, log_path: Path | None = None) -> bool:
    log = _load_log(log_path or settings.email_log_path)
    entry = log.get(day_key) or {}
    return entry.get("status") == "sent"


def register_delivery(
    day_key: str,
    status: str,
    extra: dict[str, Any] | None = None,
    log_path: Path | None = None,
) -> None:
    path = log_path or settings.email_log_path
    log = _load_log(path)
    payload = {"status": status, **(extra or {})}
    log[day_key] = payload
    _write_log(path, log)


def build_report_summary(now: datetime | None = None, csv_path: Path | None = None) -> str:
    generated = (now or datetime.now(settings.timezone)).astimezone(settings.timezone)
    counts = count_attendance(csv_path)
    return (
        f"{BODY}\n"
        f"Total de confirmaciones: {counts['total']}\n"
        f"Personas que asistirán: {counts['yes']}\n"
        f"Personas que no podrán asistir: {counts['no']}\n"
        f"Equipo niño: {counts['boy']}\n"
        f"Equipo niña: {counts['girl']}\n"
        f"Aún no lo sé: {counts['unknown']}\n"
        f"Fecha y hora de generación: {generated.isoformat()}\n"
    )


def _gmail_service(allow_interactive_auth: bool = True):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    secret = settings.google_client_secret_file
    token_path = settings.google_token_file
    if not secret.is_file():
        raise FileNotFoundError("Missing Google OAuth client secret file.")
    creds = None
    if token_path.is_file():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif allow_interactive_auth:
            flow = InstalledAppFlow.from_client_secrets_file(str(secret), SCOPES)
            creds = flow.run_local_server(port=0)
        else:
            raise RuntimeError("Gmail authorization is not configured.")
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json(), encoding="utf-8")
        token_path.chmod(0o600)
    return build("gmail", "v1", credentials=creds)


def authorize_gmail() -> None:
    """Run the one-time local OAuth consent flow without sending an email."""
    from google_auth_oauthlib.flow import InstalledAppFlow

    secret = settings.google_client_secret_file
    if not secret.is_file():
        raise FileNotFoundError("Missing Google OAuth client secret file.")
    flow = InstalledAppFlow.from_client_secrets_file(str(secret), SCOPES)
    credentials = flow.run_local_server(port=0)
    token_path = settings.google_token_file
    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(credentials.to_json(), encoding="utf-8")
    token_path.chmod(0o600)


def _message_with_attachment(summary: str, csv_path: Path) -> dict[str, str]:
    message = EmailMessage()
    message["To"] = settings.gmail_recipient
    message["From"] = settings.gmail_sender
    message["Subject"] = SUBJECT
    message.set_content(summary)
    csv_bytes = csv_path.read_bytes()
    message.add_attachment(
        csv_bytes,
        maintype="text",
        subtype="csv",
        filename="attendance.csv",
    )
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw}


def _rsvp_notification_body(records: list[dict[str, str]], generated: datetime) -> str:
    team_names = {"boy": "Team Niño", "girl": "Team Niña", "unknown": "Aún no lo sabe"}
    invitation_names = {"family": "Familiar", "individual": "Individual"}
    guest_names = "\n".join(f"- {record['name']}" for record in records)
    teams = ", ".join(
        sorted(
            {
                team_names.get(record["team"], "Sin equipo seleccionado")
                for record in records
            }
        )
    )
    return (
        "Hola,\n\n"
        "Se recibió una nueva confirmación afirmativa para la revelación de género.\n\n"
        f"Invitados:\n{guest_names}\n\n"
        f"Tipo de invitación: "
        f"{invitation_names.get(records[0]['invitation_type'], 'No especificado')}\n"
        f"Equipo seleccionado: {teams}\n"
        f"Fecha y hora de recepción: {generated.astimezone(settings.timezone).isoformat()}\n\n"
        "Saludos."
    )


def _message_for_rsvp_notification(
    records: list[dict[str, str]], generated: datetime
) -> dict[str, str]:
    message = EmailMessage()
    message["To"] = settings.gmail_recipient
    message["From"] = settings.gmail_sender
    message["Subject"] = "Nueva confirmación de asistencia - Revelación de género"
    message.set_content(_rsvp_notification_body(records, generated))
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw}


def send_rsvp_notification(
    records: list[dict[str, str]], now: datetime | None = None
) -> dict[str, Any]:
    """Notify the configured recipient about an affirmative RSVP."""
    generated = now or datetime.now(settings.timezone)
    result: dict[str, Any] = {"sent": False}
    try:
        if not settings.gmail_sender or not settings.gmail_recipient:
            raise RuntimeError("Gmail sender and recipient must be configured.")
        if not records or any(record.get("attendance") != "yes" for record in records):
            raise ValueError("RSVP notification requires affirmative attendance records.")
        service = _gmail_service(allow_interactive_auth=False)
        body = _message_for_rsvp_notification(records, generated)
        service.users().messages().send(userId="me", body=body).execute()
        result["sent"] = True
    except Exception as exc:  # noqa: BLE001 — save is independent; keep failures visible in logs
        logger.exception("Immediate RSVP Gmail notification failed")
        result["error"] = type(exc).__name__
    return result


def send_daily_report(
    now: datetime | None = None,
    csv_path: Path | None = None,
    dry_run: bool = False,
    log_path: Path | None = None,
    client_secret_file: Path | None = None,
) -> dict[str, Any]:
    """Send the attendance CSV. Never mutates the CSV on failure."""
    generated = (now or datetime.now(settings.timezone)).astimezone(settings.timezone)
    day_key = generated.date().isoformat()
    summary = build_report_summary(generated, csv_path)
    attachment = Path(export_attendance(csv_path))
    result: dict[str, Any] = {
        "sent": False,
        "day": day_key,
        "summary": summary,
        "attachment": str(attachment),
    }
    if dry_run:
        result["sent"] = True
        result["dry_run"] = True
        return result
    try:
        if client_secret_file is not None and not client_secret_file.is_file():
            raise FileNotFoundError("Missing Google OAuth client secret file.")
        service = _gmail_service()
        body = _message_with_attachment(summary, attachment)
        service.users().messages().send(userId="me", body=body).execute()
        register_delivery(
            day_key,
            "sent",
            {"sent_at": generated.isoformat()},
            log_path=log_path,
        )
        result["sent"] = True
        return result
    except Exception as exc:  # noqa: BLE001 — log and keep CSV intact
        logger.exception("Gmail delivery failed")
        register_delivery(
            day_key,
            "failed",
            {"attempted_at": generated.isoformat(), "error": type(exc).__name__},
            log_path=log_path,
        )
        result["error"] = type(exc).__name__
        return result
