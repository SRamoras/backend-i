from django.contrib import admin

from .models import ActionItem, Meeting


def mark_completed(modeladmin, request, queryset):
    queryset.update(status="completed")


mark_completed.short_description = "Mark selected action items as completed"


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "owner")
    list_filter = ("date", "owner")
    search_fields = ("title", "owner")
    # Permission for Meeting is controlled entirely by the group permissions:
    #   viewer  → view_meeting only
    #   editor  → change_meeting + view_meeting (no delete, no add)
    #   admin   → full access via superuser or explicit permissions


@admin.register(ActionItem)
class ActionItemAdmin(admin.ModelAdmin):
    list_display = ("id", "meeting", "owner", "due_date", "status")
    list_filter = ("status",)
    search_fields = ("description", "owner__username")
    actions = [mark_completed]

    # Challenge: ownership-based permissions
    # Non-superusers can only change/delete their own action items.

    def has_change_permission(self, request, obj=None):
        if not super().has_change_permission(request, obj):
            return False
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return obj.owner == request.user

    def has_delete_permission(self, request, obj=None):
        if not super().has_delete_permission(request, obj):
            return False
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return obj.owner == request.user
