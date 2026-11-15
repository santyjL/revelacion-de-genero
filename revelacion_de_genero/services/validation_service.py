"""Backend validation and sanitization for RSVP submissions."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

ATTENDANCE_VALUES = {"yes", "no"}
TEAM_VALUES = {"boy", "girl", "unknown"}
CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    message: str = ""
    name: str = ""
    attendance: str = ""
    team: str = "unknown"


def sanitize_name(raw: str | None) -> str:
    """Normalize whitespace and strip unsafe control characters."""
    value = unicodedata.normalize("NFC", raw or "")
    value = CONTROL_CHARS.sub("", value)
    return " ".join(value.split()).strip()


def sanitize_csv_field(value: str) -> str:
    """Neutralize spreadsheet formula injection."""
    if value and value[0] in {"=", "+", "-", "@", "\t", "\r"}:
        return f"'{value}"
    return value


def validate_rsvp(name: str | None, attendance: str | None, team: str | None) -> ValidationResult:
    cleaned = sanitize_name(name)
    if len(cleaned) < 2:
        return ValidationResult(False, "Escribe tu nombre (mínimo 2 caracteres).")
    if len(cleaned) > 100:
        return ValidationResult(False, "El nombre no puede superar 100 caracteres.")
    choice = (attendance or "").strip().lower()
    if choice not in ATTENDANCE_VALUES:
        return ValidationResult(False, "Confirma si podrás asistir.")
    selected_team = (team or "unknown").strip().lower()
    if selected_team not in TEAM_VALUES:
        selected_team = "unknown"
    return ValidationResult(True, name=cleaned, attendance=choice, team=selected_team)
