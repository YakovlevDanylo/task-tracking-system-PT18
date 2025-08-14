from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):

    STATUS_CHOICES = [
        ("todo", "TO DO"),
        ("in_progress", "IN PROGRESS"),
        ("complete",  "COMPLETE"),
    ]

    PRIORITY_CHOICES = [
        ("low_priority", "LOW PRIORITY"),
        ("middle_priority", "MIDDLE PRIORITY"),
        ("high_priority", "HIGH PRIORITY"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    end_time = models.DateField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.title}] - {self.creator.username}"
