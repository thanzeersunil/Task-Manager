from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    STATUS_CHOICES = [
        ("Todo", "Todo"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Todo")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="Medium")
    due_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title
