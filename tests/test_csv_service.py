from pathlib import Path

from revelacion_de_genero.services.csv_service import (
    count_attendance,
    export_attendance,
    initialize_csv,
    read_attendance,
    save_attendance,
)


def _record(name: str, attendance: str = "yes", team: str = "unknown") -> dict:
    return {
        "name": name,
        "attendance": attendance,
        "team": team,
        "submitted_at": "2026-11-14T18:30:00-06:00",
    }


def test_initialize_missing_csv(tmp_path: Path):
    path = tmp_path / "attendance.csv"
    initialize_csv(path)
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "id,name,attendance,team,submitted_at" in text


def test_append_and_preserve_records(tmp_path: Path):
    path = tmp_path / "attendance.csv"
    assert save_attendance(_record("María López", "yes", "girl"), path)
    assert save_attendance(_record("Carlos Pérez", "no", "unknown"), path)
    rows = read_attendance(path)
    assert len(rows) == 2
    assert rows[0]["name"] == "María López"
    assert rows[1]["name"] == "Carlos Pérez"
    counts = count_attendance(path)
    assert counts["total"] == 2
    assert counts["yes"] == 1
    assert counts["no"] == 1
    assert counts["girl"] == 1
    assert counts["unknown"] == 1
    assert export_attendance(path).endswith("attendance.csv")


def test_invalid_input_is_rejected(tmp_path: Path):
    path = tmp_path / "attendance.csv"
    assert not save_attendance({"name": "Solo"}, path)
    initialize_csv(path)
    assert read_attendance(path) == []


def test_utf8_roundtrip(tmp_path: Path):
    path = tmp_path / "attendance.csv"
    save_attendance(_record("José Núñez"), path)
    rows = read_attendance(path)
    assert rows[0]["name"] == "José Núñez"
