from django.db import models


class Meeting(models.Model):
    title = models.CharField(max_length=150)
    date = models.DateField()
    owner = models.CharField(max_length=100)


class ActionItem(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name="action_items")
    description = models.CharField(max_length=300)
    owner = models.CharField(max_length=100)
    due_date = models.DateField()
    status = models.CharField(max_length=20, default="open")
