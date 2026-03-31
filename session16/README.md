# Session 16 | Django Admin

## Objective
Operate data productively through the Django admin interface.

## Setup

```bash
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Access admin at: http://127.0.0.1:8000/admin/

## What was implemented

### `meetings/admin.py`

#### Exercise — `MeetingAdmin`
- `list_display`: shows `id`, `title`, `date`, `owner` as columns
- `list_filter`: filter sidebar by `date` and `owner`
- `search_fields`: full-text search on `title` and `owner`

#### Challenge — `ActionItemAdmin` with custom action
- `list_display`: shows `id`, `meeting`, `owner`, `due_date`, `status`
- `list_filter`: filter sidebar by `status`
- `search_fields`: full-text search on `description` and `owner`
- `actions`: custom action `mark_completed` — bulk-sets `status = "completed"` on selected rows

## Verification
- Admin allows create / edit / list / search on both `Meeting` and `ActionItem`
- Selecting multiple `ActionItem` rows and applying "Mark selected action items as completed" updates their status in bulk
