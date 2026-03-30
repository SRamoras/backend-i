from datetime import datetime
from core.errors import ValidationError


def validate_iso_date(value: str) -> None:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValidationError("Date must be YYYY-MM-DD") from exc


def validate_required(value, field_name: str):
    if not value:
        raise ValidationError(f"{field_name} is required")