from django.db import models
from django.utils import timezone

from .base import TimeStampedModel
from datetime import datetime

# Create your models here.
class Task(TimeStampedModel):
    title = models.CharField(max_length=200,help_text='Task title')
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(default=lambda :timezone.make_aware(datetime.now(), timezone.get_current_timezone()), blank=True, null=True)
    status = models.CharField(max_length=10,choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    priority = models.CharField(max_length=10,choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low')
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
     