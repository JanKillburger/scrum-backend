from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = {'open': 'Open', 'completed': 'Completed'}
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    due_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', editable=False)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')


