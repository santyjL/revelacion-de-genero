from pathlib import Path

from revelacion_de_genero.services.csv_service import (
    count_attendance,
    export_attendance,
    initialize_csv,
    read_attendance,
    save_attendance,
    save_attendance_batch,
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
    assert "id,invitation_id,invitation_type,name,attendance,team,submitted_at" in text


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


def test_family_records_share_invitation_and_count_each_person(tmp_path: Path):
    path = tmp_path / "attendance.csv"
    records = [
        {
            **_record(name, "yes", "girl"),
            "invitation_id": "family-123",
            "invitation_type": "family",
        }
        for name in ("María López", "José López", "Ana López")
    ]

    assert save_attendance_batch(records, path)

    rows = read_attendance(path)
    assert [row["name"] for row in rows] == ["María López", "José López", "Ana López"]
    assert {row["invitation_id"] for row in rows} == {"family-123"}
    assert {row["invitation_type"] for row in rows} == {"family"}
    assert count_attendance(path)["total"] == 3
    assert count_attendance(path)["yes"] == 3


def test_legacy_csv_is_preserved_when_appending(tmp_path: Path):
    path = tmp_path / "attendance.csv"
    path.write_text(
        "id,name,attendance,team,submitted_at\n"
        "1,María López,yes,girl,2026-11-14T18:30:00-06:00\n",
        encoding="utf-8",
    )

    assert save_attendance(_record("Carlos Pérez", team="boy"), path)

    rows = read_attendance(path)
    assert len(rows) == 2
    assert rows[0]["name"] == "María López"
    assert rows[0]["invitation_type"] == "individual"
    assert rows[1]["name"] == "Carlos Pérez"
