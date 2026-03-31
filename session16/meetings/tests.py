from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .admin import ActionItemAdmin, MeetingAdmin, mark_completed
from .models import ActionItem, Meeting


class MeetingAdminConfigTest(TestCase):
    def test_list_display(self):
        self.assertEqual(MeetingAdmin.list_display, ("id", "title", "date", "owner"))

    def test_list_filter(self):
        self.assertEqual(MeetingAdmin.list_filter, ("date", "owner"))

    def test_search_fields(self):
        self.assertEqual(MeetingAdmin.search_fields, ("title", "owner"))


class ActionItemAdminConfigTest(TestCase):
    def test_list_display(self):
        self.assertEqual(
            ActionItemAdmin.list_display,
            ("id", "meeting", "owner", "due_date", "status"),
        )

    def test_list_filter(self):
        self.assertEqual(ActionItemAdmin.list_filter, ("status",))

    def test_search_fields(self):
        self.assertIn("owner", ActionItemAdmin.search_fields)

    def test_mark_completed_action_registered(self):
        self.assertIn(mark_completed, ActionItemAdmin.actions)


class MeetingAdminViewTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", password="admin123", email="admin@test.com"
        )
        self.client.force_login(self.admin_user)
        self.meeting = Meeting.objects.create(
            title="Sprint Review", date="2026-03-31", owner="alice"
        )

    def test_changelist_loads(self):
        url = reverse("admin:meetings_meeting_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_search_by_title(self):
        url = reverse("admin:meetings_meeting_changelist") + "?q=Sprint"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sprint Review")

    def test_search_no_match(self):
        url = reverse("admin:meetings_meeting_changelist") + "?q=xyz_no_match"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Sprint Review")

    def test_filter_by_owner(self):
        url = reverse("admin:meetings_meeting_changelist") + "?owner=alice"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_view_loads(self):
        url = reverse("admin:meetings_meeting_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ActionItemAdminViewTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", password="admin123", email="admin@test.com"
        )
        self.client.force_login(self.admin_user)
        self.meeting = Meeting.objects.create(
            title="Planning", date="2026-03-31", owner="bob"
        )
        self.item1 = ActionItem.objects.create(
            meeting=self.meeting,
            description="Fix bug",
            owner="bob",
            due_date="2026-04-10",
            status="open",
        )
        self.item2 = ActionItem.objects.create(
            meeting=self.meeting,
            description="Write docs",
            owner="carol",
            due_date="2026-04-15",
            status="open",
        )

    def test_changelist_loads(self):
        url = reverse("admin:meetings_actionitem_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_filter_by_status(self):
        url = reverse("admin:meetings_actionitem_changelist") + "?status__exact=open"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_search_by_owner(self):
        url = reverse("admin:meetings_actionitem_changelist") + "?q=carol"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "carol")

    def test_mark_completed_action(self):
        url = reverse("admin:meetings_actionitem_changelist")
        data = {
            "action": "mark_completed",
            "_selected_action": [self.item1.pk, self.item2.pk],
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.item1.refresh_from_db()
        self.item2.refresh_from_db()
        self.assertEqual(self.item1.status, "completed")
        self.assertEqual(self.item2.status, "completed")

    def test_mark_completed_partial(self):
        url = reverse("admin:meetings_actionitem_changelist")
        data = {
            "action": "mark_completed",
            "_selected_action": [self.item1.pk],
        }
        self.client.post(url, data, follow=True)
        self.item1.refresh_from_db()
        self.item2.refresh_from_db()
        self.assertEqual(self.item1.status, "completed")
        self.assertEqual(self.item2.status, "open")
