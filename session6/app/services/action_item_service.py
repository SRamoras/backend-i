import logging
from core.errors import ValidationError
from core.validators import validate_iso_date, validate_required

logger = logging.getLogger(__name__)

def create_action_item(title: str, owner: str, due_date: str):
    logger.info("Creating action item: %s", title)

    try:
        validate_required(title, "title")
        validate_required(owner, "owner")
        validate_required(due_date, "due_date")
        validate_iso_date(due_date)
    except ValidationError as exc:
        logger.warning("Validation failed: %s", exc)
        raise

    action_item = {
        "title": title,
        "owner": owner,
        "due_date": due_date,
    }

    logger.info("Action item created successfully: %s", title)
    return action_item