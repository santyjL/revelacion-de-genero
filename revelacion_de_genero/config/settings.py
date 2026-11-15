"""Centralized, environment-driven application settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


@dataclass(frozen=True)
class Settings:
    """Runtime configuration for the invitation, RSVP storage and reports."""

    timezone_name: str = _env("EVENT_TIMEZONE", "America/Managua")
    event_date: date = date.fromisoformat(_env("EVENT_DATE", "2026-11-29"))
    event_time: time = time.fromisoformat(_env("EVENT_TIME", "15:00:00"))
    event_place: str = _env("EVENT_PLACE", "Restaurante Pikito's")
    report_end_date: date = date.fromisoformat(_env("REPORT_END_DATE", "2026-11-22"))
    data_dir: Path = PROJECT_ROOT / "data"
    attendance_csv: Path = PROJECT_ROOT / "data" / "attendance.csv"
    email_log_path: Path = PROJECT_ROOT / "data" / "email_log.json"
    credentials_dir: Path = PROJECT_ROOT / "credentials"
    gmail_sender: str = _env("GMAIL_SENDER")
    gmail_recipient: str = _env("GMAIL_RECIPIENT")
    google_client_secret_file: Path = Path(
        _env("GOOGLE_CLIENT_SECRET_FILE", str(PROJECT_ROOT / "credentials" / "client_secret.json"))
    )
    google_token_file: Path = Path(
        _env("GOOGLE_TOKEN_FILE", str(PROJECT_ROOT / "credentials" / "token.json"))
    )
    bible_verse_text: str = _env("BIBLE_VERSE_TEXT")
    bible_verse_reference: str = _env("BIBLE_VERSE_REFERENCE")
    rsvp_min_seconds: int = int(_env("RSVP_MIN_SECONDS", "8"))
    assets_dir: Path = PROJECT_ROOT / "assets"

    @property
    def timezone(self) -> ZoneInfo:
        return ZoneInfo(self.timezone_name)

    @property
    def event_datetime(self) -> datetime:
        return datetime.combine(self.event_date, self.event_time, tzinfo=self.timezone)

    @property
    def event_deadline_ms(self) -> int:
        return int(self.event_datetime.timestamp() * 1000)

    @property
    def baby_photo_src(self) -> str | None:
        photo = self.assets_dir / "baby_photo.jpg"
        if photo.is_file():
            return "/baby_photo.jpg"
        return None

    @property
    def ultrasound_video_src(self) -> str | None:
        video = self.assets_dir / "ultrasonido.mp4"
        if video.is_file():
            return "/ultrasonido.mp4"
        return None


settings = Settings()
