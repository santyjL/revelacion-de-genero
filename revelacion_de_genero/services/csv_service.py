"""CSV persistence for individual and family attendance records."""

from __future__ import annotations

import csv
import fcntl
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4
from zoneinfo import ZoneInfo

from revelacion_de_genero.config.settings import settings
from revelacion_de_genero.services.validation_service import sanitize_csv_field

COLUMNS = [
    "id",
    "invitation_id",
    "invitation_type",
    "name",
    "attendance",
    "team",
    "submitted_at",
]
LEGACY_COLUMNS = ["id", "name", "attendance", "team", "submitted_at"]
REQUIRED_FIELDS = {"name", "attendance", "team", "submitted_at"}


def initialize_csv(path: Path | None = None) -> None:
    """Create the attendance file with headers if it does not exist."""
    csv_path = path or settings.attendance_csv
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    if csv_path.exists():
        return
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=COLUMNS).writeheader()


def _lock_file(handle) -> None:
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX)


def _unlock_file(handle) -> None:
    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _read_rows(handle) -> list[dict[str, str]]:
    handle.seek(0)
    reader = csv.DictReader(handle)
    if reader.fieldnames is None:
        return []
    if reader.fieldnames == COLUMNS:
        return [row for row in reader if any(row.values())]
    if reader.fieldnames == LEGACY_COLUMNS:
        return [
            {
                **row,
                "invitation_id": f"legacy-{row.get('id', '')}",
                "invitation_type": "individual",
            }
            for row in reader
            if any(row.values())
        ]
    raise ValueError("The attendance CSV has an unsupported header.")


def read_attendance(path: Path | None = None) -> list[dict[str, str]]:
    csv_path = path or settings.attendance_csv
    initialize_csv(csv_path)
    with csv_path.open("r+", encoding="utf-8", newline="") as handle:
        _lock_file(handle)
        try:
            return _read_rows(handle)
        finally:
            _unlock_file(handle)


def save_attendance_batch(records: list[dict[str, Any]], path: Path | None = None) -> bool:
    """Append all members of one invitation while holding a single file lock."""
    if not records or any(REQUIRED_FIELDS - set(record) for record in records):
        return False
    if any(
        not str(record.get("name", "")).strip()
        or record.get("attendance") not in {"yes", "no"}
        or record.get("team") not in {"boy", "girl", "unknown"}
        or record.get("invitation_type", "individual") not in {"individual", "family"}
        for record in records
    ):
        return False

    csv_path = path or settings.attendance_csv
    try:
        initialize_csv(csv_path)
        with csv_path.open("r+", encoding="utf-8", newline="") as handle:
            _lock_file(handle)
            try:
                existing_rows = _read_rows(handle)
                existing_ids = [
                    int(row["id"])
                    for row in existing_rows
                    if str(row.get("id", "")).isdigit()
                ]
                next_id = max(existing_ids, default=0) + 1
                fallback_invitation_id = uuid4().hex
                payloads = [
                    {
                        "id": str(next_id + index),
                        "invitation_id": sanitize_csv_field(
                            str(record.get("invitation_id") or fallback_invitation_id)
                        ),
                        "invitation_type": sanitize_csv_field(
                            str(record.get("invitation_type", "individual"))
                        ),
                        "name": sanitize_csv_field(str(record["name"])),
                        "attendance": sanitize_csv_field(str(record["attendance"])),
                        "team": sanitize_csv_field(str(record["team"])),
                        "submitted_at": sanitize_csv_field(str(record["submitted_at"])),
                    }
                    for index, record in enumerate(records)
                ]
                handle.seek(0)
                header = next(csv.reader(handle), [])
                if header == COLUMNS:
                    handle.seek(0, 2)
                    csv.DictWriter(handle, fieldnames=COLUMNS).writerows(payloads)
                else:
                    handle.seek(0)
                    writer = csv.DictWriter(handle, fieldnames=COLUMNS)
                    writer.writeheader()
                    writer.writerows(existing_rows)
                    writer.writerows(payloads)
                    handle.truncate()
                handle.flush()
                return True
            finally:
                _unlock_file(handle)
    except (OSError, ValueError, csv.Error):
        return False


def save_attendance(record: dict[str, Any], path: Path | None = None) -> bool:
    """Append one attendance record, retaining the existing service API."""
    return save_attendance_batch([record], path)


def count_attendance(path: Path | None = None) -> dict[str, int]:
    rows = read_attendance(path)
    counts = {
        "total": len(rows),
        "yes": 0,
        "no": 0,
        "boy": 0,
        "girl": 0,
        "unknown": 0,
    }
    for row in rows:
        attendance = row.get("attendance", "")
        if attendance in {"yes", "no"}:
            counts[attendance] += 1
        team = row.get("team", "unknown")
        if team in {"boy", "girl", "unknown"}:
            counts[team] += 1
        else:
            counts["unknown"] += 1
    return counts


def export_attendance(path: Path | None = None) -> str:
    csv_path = path or settings.attendance_csv
    initialize_csv(csv_path)
    return str(csv_path)


def recent_duplicate(name: str, seconds: int = 120, path: Path | None = None) -> bool:
    """Detect an accidental repeat of the same guest name."""
    rows = read_attendance(path)
    now = datetime.now(ZoneInfo(settings.timezone_name))
    needle = name.casefold()
    for row in reversed(rows):
        if row.get("name", "").casefold() != needle:
            continue
        try:
            submitted = datetime.fromisoformat(row["submitted_at"])
        except (KeyError, ValueError):
            return True
        if submitted.tzinfo is None:
            submitted = submitted.replace(tzinfo=now.tzinfo)
        return abs((now - submitted).total_seconds()) < seconds
    return False
