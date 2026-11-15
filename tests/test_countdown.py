from datetime import datetime
from zoneinfo import ZoneInfo

from revelacion_de_genero.config.settings import settings
from revelacion_de_genero.services.countdown_service import (
    event_deadline,
    is_event_started,
    remaining_parts,
)


def test_deadline_and_timezone():
    deadline = event_deadline()
    assert deadline.tzinfo == ZoneInfo("America/Managua")
    assert deadline.year == 2026
    assert deadline.month == 11
    assert deadline.day == 29
    assert deadline.hour == 15
    assert deadline.minute == 0


def test_transition_to_zero():
    tz = settings.timezone
    before = datetime(2026, 11, 29, 14, 59, 1, tzinfo=tz)
    at_start = datetime(2026, 11, 29, 15, 0, 0, tzinfo=tz)
    after = datetime(2026, 11, 29, 15, 0, 1, tzinfo=tz)
    parts = remaining_parts(before)
    assert parts is not None
    assert parts["seconds"] == 59
    assert remaining_parts(at_start) is None
    assert is_event_started(at_start)
    assert is_event_started(after)
