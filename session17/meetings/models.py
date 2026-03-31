from django.conf import settings
from django.db import models


class Meeting(models.Model):
    title = models.CharField(max_length=150)
    date = models.DateField()
    owner = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ActionItem(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name="action_items")
    description = models.CharField(max_length=300)
    # FK to User enables ownership-based permission checks
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="action_items",
    )
    due_date = models.DateField()
    status = models.CharField(max_length=20, default="open")

    def __str__(self):
        return self.description
