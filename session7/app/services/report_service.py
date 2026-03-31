from domain.models import ActionItem

def summary(items: list[ActionItem]) -> dict:
    return {
        "total": len(items),
        "by_owner": _group_by_owner(items),
    }

def _group_by_owner(items: list[ActionItem]) -> dict:
    result = {}
    for item in items:
        result[item.owner] = result.get(item.owner, 0) + 1
    return result

def period_report(items: list[ActionItem], from_date: str, to_date: str) -> dict:
    filtered = [i for i in items if from_date <= i.due_date <= to_date]
    return {
        "from": from_date,
        "to": to_date,
        "total": len(filtered),
        "items": [i.__dict__ for i in filtered],
    }