from core.errors import ValidationError
from core.validators import validate_iso_date, validate_required


def create_action_item(title: str, owner: str, due_date: str):
    validate_required(title, "title")
    validate_required(owner, "owner")
    validate_required(due_date, "due_date")

    validate_iso_date(due_date)

    # fake database
    action_item = {
        "title": title,
        "owner": owner,
        "due_date": due_date,
    }

    return action_item