import datetime

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Group, Permission, User
from django.test import RequestFactory, TestCase

from .admin import ActionItemAdmin, MeetingAdmin
from .models import ActionItem, Meeting


def make_meeting():
    return Meeting.objects.create(title="Sprint Review", date=datetime.date.today(), owner="team")


def make_user(username, password="pass1234!", groups=(), permissions=()):
    user = User.objects.create_user(username=username, password=password)
    for group in groups:
        user.groups.add(group)
    for perm in permissions:
        user.user_permissions.add(perm)
    return user


class GroupSetupMixin(TestCase):
    """Create viewer / editor groups with the correct permissions."""

    @classmethod
    def setUpTestData(cls):
        change_meeting = Permission.objects.get(codename="change_meeting")
        view_meeting = Permission.objects.get(codename="view_meeting")

        cls.editor_group, _ = Group.objects.get_or_create(name="editor")
        cls.editor_group.permissions.set([change_meeting, view_meeting])

        cls.viewer_group, _ = Group.objects.get_or_create(name="viewer")
        cls.viewer_group.permissions.set([view_meeting])


# ---------------------------------------------------------------------------
# Exercise: viewer cannot edit meetings; editor cannot delete meetings
# ---------------------------------------------------------------------------

class MeetingGroupPermissionsTest(GroupSetupMixin):

    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()
        self.meeting = make_meeting()

    def _make_request(self, user):
        request = self.factory.get("/")
        request.user = user
        return request

    def test_viewer_cannot_change_meeting(self):
        viewer = make_user("viewer1", groups=[self.viewer_group])
        request = self._make_request(viewer)
        ma = MeetingAdmin(Meeting, self.site)
        self.assertFalse(ma.has_change_permission(request, self.meeting))

    def test_viewer_can_view_meeting(self):
        viewer = make_user("viewer2", groups=[self.viewer_group])
        request = self._make_request(viewer)
        ma = MeetingAdmin(Meeting, self.site)
        self.assertTrue(ma.has_view_permission(request, self.meeting))

    def test_editor_can_change_meeting(self):
        editor = make_user("editor1", groups=[self.editor_group])
        request = self._make_request(editor)
        ma = MeetingAdmin(Meeting, self.site)
        self.assertTrue(ma.has_change_permission(request, self.meeting))

    def test_editor_cannot_delete_meeting(self):
        editor = make_user("editor2", groups=[self.editor_group])
        request = self._make_request(editor)
        ma = MeetingAdmin(Meeting, self.site)
        self.assertFalse(ma.has_delete_permission(request, self.meeting))

    def test_superuser_can_delete_meeting(self):
        superuser = User.objects.create_superuser("super1", password="pass1234!")
        request = self._make_request(superuser)
        ma = MeetingAdmin(Meeting, self.site)
        self.assertTrue(ma.has_delete_permission(request, self.meeting))


# ---------------------------------------------------------------------------
# Challenge: ownership-based permissions for ActionItems
# ---------------------------------------------------------------------------

class ActionItemOwnershipPermissionsTest(GroupSetupMixin):

    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()
        self.meeting = make_meeting()

        delete_ai = Permission.objects.get(codename="delete_actionitem")
        change_ai = Permission.objects.get(codename="change_actionitem")

        self.alice = make_user("alice", permissions=[change_ai, delete_ai])
        self.bob = make_user("bob", permissions=[change_ai, delete_ai])

        self.alice_item = ActionItem.objects.create(
            meeting=self.meeting,
            description="Alice's task",
            owner=self.alice,
            due_date=datetime.date.today(),
        )
        self.bob_item = ActionItem.objects.create(
            meeting=self.meeting,
            description="Bob's task",
            owner=self.bob,
            due_date=datetime.date.today(),
        )

    def _request(self, user):
        request = self.factory.get("/")
        request.user = user
        return request

    def test_owner_can_change_own_action_item(self):
        request = self._request(self.alice)
        aia = ActionItemAdmin(ActionItem, self.site)
        self.assertTrue(aia.has_change_permission(request, self.alice_item))

    def test_owner_cannot_change_others_action_item(self):
        request = self._request(self.alice)
        aia = ActionItemAdmin(ActionItem, self.site)
        self.assertFalse(aia.has_change_permission(request, self.bob_item))

    def test_owner_can_delete_own_action_item(self):
        request = self._request(self.bob)
        aia = ActionItemAdmin(ActionItem, self.site)
        self.assertTrue(aia.has_delete_permission(request, self.bob_item))

    def test_owner_cannot_delete_others_action_item(self):
        request = self._request(self.bob)
        aia = ActionItemAdmin(ActionItem, self.site)
        self.assertFalse(aia.has_delete_permission(request, self.alice_item))

    def test_superuser_can_change_any_action_item(self):
        superuser = User.objects.create_superuser("super2", password="pass1234!")
        request = self._request(superuser)
        aia = ActionItemAdmin(ActionItem, self.site)
        self.assertTrue(aia.has_change_permission(request, self.bob_item))

    def test_superuser_can_delete_any_action_item(self):
        superuser = User.objects.create_superuser("super3", password="pass1234!")
        request = self._request(superuser)
        aia = ActionItemAdmin(ActionItem, self.site)
        self.assertTrue(aia.has_delete_permission(request, self.alice_item))

    def test_list_permission_not_restricted_by_ownership(self):
        """has_change_permission with no obj (list view) should return True for permitted users."""
        request = self._request(self.alice)
        aia = ActionItemAdmin(ActionItem, self.site)
        self.assertTrue(aia.has_change_permission(request))
