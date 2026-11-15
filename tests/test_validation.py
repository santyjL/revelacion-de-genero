from revelacion_de_genero.services.validation_service import (
    sanitize_csv_field,
    sanitize_name,
    validate_rsvp,
)


def test_valid_name_and_yes_attendance():
    result = validate_rsvp("  María López  ", "yes", "girl")
    assert result.ok
    assert result.name == "María López"
    assert result.attendance == "yes"
    assert result.team == "girl"


def test_empty_name():
    result = validate_rsvp("   ", "yes", "boy")
    assert not result.ok


def test_spanish_characters():
    result = validate_rsvp("José Núñez", "no", "boy")
    assert result.ok
    assert result.name == "José Núñez"
    assert result.attendance == "no"


def test_both_attendance_options():
    assert validate_rsvp("Ana", "yes", "boy").ok
    assert validate_rsvp("Ana", "no", "girl").ok
    assert not validate_rsvp("Ana", "", "boy").ok
    assert not validate_rsvp("Ana", "yes", "").ok


def test_each_team_selection():
    for team in ("boy", "girl"):
        result = validate_rsvp("Carlos Pérez", "yes", team)
        assert result.ok
        assert result.team == team
    assert not validate_rsvp("Carlos Pérez", "yes", "unknown").ok


def test_csv_formula_injection():
    assert sanitize_csv_field("=2+2").startswith("'")
    assert sanitize_name("  Ana\tMaría  ") == "Ana María"
