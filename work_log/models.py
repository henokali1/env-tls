from django.db import models
from django.contrib.auth.models import User
import datetime

class Tag(models.Model):
    COLOR_CHOICES = [
        ('#3b82f6', 'Blue'),
        ('#10b981', 'Green'),
        ('#f59e0b', 'Amber'),
        ('#ef4444', 'Red'),
        ('#8b5cf6', 'Purple'),
        ('#ec4899', 'Pink'),
        ('#6b7280', 'Gray'),
        ('#14b8a6', 'Teal'),
    ]
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#3b82f6')
    
    def __str__(self):
        return self.name

class WorkLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    task_description = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
