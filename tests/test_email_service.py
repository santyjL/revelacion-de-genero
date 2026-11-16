import base64
from email import message_from_bytes, policy
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from zoneinfo import ZoneInfo

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


def test_rsvp_notification_attaches_csv_for_configured_recipient(monkeypatch, tmp_path: Path):
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
    csv_path = tmp_path / "attendance.csv"
    csv_path.write_text("id,name\n1,María López\n", encoding="utf-8")
    monkeypatch.setattr(
        email_service,
        "_gmail_service",
        lambda allow_interactive_auth: fake_service,
    )
    monkeypatch.setattr(email_service, "export_attendance", lambda: str(csv_path))
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
    assert message["To"] == email_service.settings.email_recipient
    assert message["From"] == email_service.settings.email_sender
    body = message.get_body(preferencelist=("plain",)).get_content()
    assert "María López" in body
    assert "Team Niña" in body
    attachment = next(part for part in message.iter_attachments())
    assert attachment.get_filename() == "attendance.csv"
    attached_csv = attachment.get_payload(decode=True).decode("utf-8")
    assert "María López" in attached_csv


def test_negative_rsvp_is_sent_with_csv_attachment(monkeypatch, tmp_path: Path):
    sent = {}

    class FakeMessages:
        def send(self, userId, body):
            sent["body"] = body
            return SimpleNamespace(execute=lambda: {"id": "message-id"})

    fake_service = SimpleNamespace(users=lambda: SimpleNamespace(messages=lambda: FakeMessages()))
    csv_path = tmp_path / "attendance.csv"
    csv_path.write_text("id,name\n1,Alex\n", encoding="utf-8")
    monkeypatch.setattr(
        email_service,
        "_gmail_service",
        lambda allow_interactive_auth: fake_service,
    )
    monkeypatch.setattr(email_service, "export_attendance", lambda: str(csv_path))
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
    message = message_from_bytes(
        base64.urlsafe_b64decode(sent["body"]["raw"].encode("utf-8")),
        policy=policy.default,
    )
    assert result["sent"] is True
    assert "No podrá asistir" in message.get_body(preferencelist=("plain",)).get_content()
    assert next(message.iter_attachments()).get_filename() == "attendance.csv"


def test_smtp_rsvp_sends_csv_over_starttls(monkeypatch, tmp_path: Path):
    sent = {}

    class FakeSMTP:
        def __init__(self, host, port, timeout):
            sent["connection"] = (host, port, timeout)

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def ehlo(self):
            sent["ehlo"] = True

        def starttls(self, context):
            sent["starttls"] = context

        def login(self, username, password):
            sent["login"] = (username, password)

        def send_message(self, message):
            sent["message"] = message

    csv_path = tmp_path / "attendance.csv"
    csv_path.write_text("id,name\n1,Ana\n", encoding="utf-8")
    monkeypatch.setattr(email_service, "export_attendance", lambda: str(csv_path))
    monkeypatch.setattr(email_service.smtplib, "SMTP", FakeSMTP)
    monkeypatch.setattr(
        email_service,
        "settings",
        SimpleNamespace(
            email_transport="smtp",
            email_sender="sender@example.com",
            email_recipient="recipient@example.com",
            smtp_host="mail.example.com",
            smtp_port=587,
            smtp_security="starttls",
            smtp_username="smtp-user",
            smtp_password="smtp-password",
            timezone=ZoneInfo("America/Managua"),
        ),
    )

    result = email_service.send_rsvp_notification(
        [{"name": "Ana", "attendance": "yes", "team": "unknown", "invitation_type": "individual"}]
    )

    assert result["sent"] is True
    assert sent["connection"] == ("mail.example.com", 587, 30)
    assert sent["starttls"] is not None
    assert sent["login"] == ("smtp-user", "smtp-password")
    assert next(sent["message"].iter_attachments()).get_filename() == "attendance.csv"


def test_report_window_includes_november_22():
    tz = ZoneInfo("America/Managua")
    assert is_report_date_active(datetime(2026, 11, 22, 20, 0, tzinfo=tz))
    assert is_report_date_active(datetime(2026, 11, 14, 20, 0, tzinfo=tz))
    assert not is_report_date_active(datetime(2026, 11, 23, 0, 1, tzinfo=tz))
