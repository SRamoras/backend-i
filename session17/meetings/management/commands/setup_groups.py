from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create groups (admin, editor, viewer) with Meeting permissions"

    def handle(self, *args, **options):
        admin_group, _ = Group.objects.get_or_create(name="admin")
        editor_group, _ = Group.objects.get_or_create(name="editor")
        viewer_group, _ = Group.objects.get_or_create(name="viewer")

        change_meeting = Permission.objects.get(codename="change_meeting")
        view_meeting = Permission.objects.get(codename="view_meeting")

        # Exercise: editor gets change + view, but NOT delete
        editor_group.permissions.set([change_meeting, view_meeting])
        viewer_group.permissions.set([view_meeting])
        # admin group gets no extra permissions here — use superuser or assign manually

        self.stdout.write(self.style.SUCCESS("Groups configured:"))
        self.stdout.write(f"  admin  → no extra permissions (use superuser flag)")
        self.stdout.write(f"  editor → change_meeting, view_meeting")
        self.stdout.write(f"  viewer → view_meeting")
