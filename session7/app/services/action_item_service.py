import logging
from domain.models import ActionItem
from core.errors import ValidationError, NotFoundError
from core.validators import validate_iso_date, validate_required
from repositories import action_item_repository as repo

logger = logging.getLogger(__name__)

def create_action_item(title: str, owner: str, due_date: str) -> ActionItem:
    logger.info("Creating action item: %s", title)
    try:
        validate_required(title, "title")
        validate_required(owner, "owner")
        validate_required(due_date, "due_date")
        validate_iso_date(due_date)
    except ValidationError as exc:
        logger.warning("Validation failed: %s", exc)
        raise
    item = ActionItem(title=title, owner=owner, due_date=due_date)
    logger.info("Action item created: %s", item.id)
    return repo.save(item)

def list_action_items() -> list[ActionItem]:
    return repo.find_all()

def get_action_item(id: str) -> ActionItem:
    item = repo.find_by_id(id)
    if not item:
        raise NotFoundError(f"Action item {id} not found")
    return item

def delete_action_item(id: str) -> None:
    if not repo.delete_by_id(id):
        raise NotFoundError(f"Action item {id} not found")