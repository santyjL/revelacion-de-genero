import base64
from email import message_from_bytes, policy
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest

from revelacion_de_genero.services.countdown_service import is_report_date_active
from revelacion_de_genero.services.csv_service import save_attendance
from revelacion_de_genero.services import email_service


def test_generate_report_includes_counts(tmp_path: Path):
    csv_path = tmp_path / "attendance.csv"
    save_attendance(
        {
            "name": "María López",
            "attendance": "yes",
            "team": "girl",
            "submitted_at": "2026-11-14T18:30:00-06:00",
        },
        csv_path,
    )
    summary = email_service.build_report_summary(
        datetime(2026, 11, 14, 20, 0, tzinfo=ZoneInfo("America/Managua")),
        csv_path,
    )
    assert "Total de confirmaciones: 1" in summary
    assert "Personas que asistirán: 1" in summary
    assert "Adjunto" in summary


def test_duplicate_prevention_and_retry(tmp_path: Path):
    log_path = tmp_path / "email_log.json"
    email_service.register_delivery("2026-11-14", "failed", {"error": "Timeout"}, log_path)
    assert not email_service.already_sent("2026-11-14", log_path)
    email_service.register_delivery(
        "2026-11-14", "sent", {"sent_at": "2026-11-14T20:00:00-06:00"}, log_path
    )
    assert email_service.already_sent("2026-11-14", log_path)


def test_failed_delivery_does_not_claim_success(tmp_path: Path):
    csv_path = tmp_path / "attendance.csv"
    result = email_service.send_daily_report(
        now=datetime(2026, 11, 14, 20, 0, tzinfo=ZoneInfo("America/Managua")),
        csv_path=csv_path,
        log_path=tmp_path / "email_log.json",
        client_secret_file=tmp_path / "missing.json",
    )
    assert result["sent"] is False
    assert result["error"] == "FileNotFoundError"
    assert csv_path.exists()


def test_affirmative_rsvp_sends_notification_to_configured_recipient(monkeypatch):
    sent = {}

    class FakeMessages:
        def send(self, userId, body):
            sent["user_id"] = userId
            sent["body"] = body
            return SimpleNamespace(execute=lambda: {"id": "message-id"})

    class FakeUsers:
        def messages(self):
            return FakeMessages()

    fake_service = SimpleNamespace(users=lambda: FakeUsers())
    monkeypatch.setattr(
        email_service,
        "_gmail_service",
        lambda allow_interactive_auth: fake_service,
    )
    records = [
        {
            "name": "María López",
            "attendance": "yes",
            "team": "girl",
            "invitation_type": "family",
        }
    ]

    result = email_service.send_rsvp_notification(
        records,
        now=datetime(2026, 11, 15, 20, 0, tzinfo=ZoneInfo("America/Managua")),
    )

    message = message_from_bytes(
        base64.urlsafe_b64decode(sent["body"]["raw"].encode("utf-8")),
        policy=policy.default,
    )
    assert result["sent"] is True
    assert sent["user_id"] == "me"
    assert message["To"] == email_service.settings.gmail_recipient
    assert message["From"] == email_service.settings.gmail_sender
    assert "María López" in message.get_content()
    assert "Team Niña" in message.get_content()


def test_rsvp_notification_does_not_send_negative_responses(monkeypatch):
    def unexpected_send(*args, **kwargs):
        pytest.fail("Gmail must not be called for a negative response.")

    monkeypatch.setattr(email_service, "_gmail_service", unexpected_send)
    result = email_service.send_rsvp_notification(
        [
            {
                "name": "Alex",
                "attendance": "no",
                "team": "unknown",
                "invitation_type": "individual",
            }
        ]
    )
    assert result == {"sent": False, "error": "ValueError"}


def test_report_window_includes_november_22():
    tz = ZoneInfo("America/Managua")
    assert is_report_date_active(datetime(2026, 11, 22, 20, 0, tzinfo=tz))
    assert is_report_date_active(datetime(2026, 11, 14, 20, 0, tzinfo=tz))
    assert not is_report_date_active(datetime(2026, 11, 23, 0, 1, tzinfo=tz))
