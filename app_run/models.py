from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS = [
    ('init', 'Init'),
    ('in_progress', 'In progress'),
    ('finished', 'Finished'),
]

class Run(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='runs')
    comment = models.TextField()
    status = models.CharField(choices=STATUS, default='init')
