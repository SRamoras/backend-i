from django.contrib import admin
from .models import Meeting, ActionItem


def mark_completed(modeladmin, request, queryset):
    queryset.update(status="completed")


mark_completed.short_description = "Mark selected action items as completed"


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "owner")
    list_filter = ("date", "owner")
    search_fields = ("title", "owner")


@admin.register(ActionItem)
class ActionItemAdmin(admin.ModelAdmin):
    list_display = ("id", "meeting", "owner", "due_date", "status")
    list_filter = ("status",)
    search_fields = ("description", "owner")
    actions = [mark_completed]
