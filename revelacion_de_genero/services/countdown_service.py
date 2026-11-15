"""Event deadline helpers independent of the visitor's timezone."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from revelacion_de_genero.config.settings import settings


def event_deadline(now: datetime | None = None) -> datetime:
    """Return the configured event instant in America/Managua."""
    del now
    return settings.event_datetime


def remaining_delta(now: datetime | None = None) -> timedelta:
    current = now or datetime.now(settings.timezone)
    if current.tzinfo is None:
        current = current.replace(tzinfo=settings.timezone)
    return event_deadline() - current.astimezone(settings.timezone)


def is_event_started(now: datetime | None = None) -> bool:
    return remaining_delta(now).total_seconds() <= 0


def remaining_parts(now: datetime | None = None) -> dict[str, int] | None:
    delta = remaining_delta(now)
    seconds = int(delta.total_seconds())
    if seconds <= 0:
        return None
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    return {"days": days, "hours": hours, "minutes": minutes, "seconds": secs}


def is_report_date_active(now: datetime | None = None) -> bool:
    """Daily reports run through November 22, 2026 inclusive."""
    current = now or datetime.now(settings.timezone)
    local_day: date = current.astimezone(settings.timezone).date()
    return local_day <= settings.report_end_date
