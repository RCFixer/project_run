from django.core.validators import MinValueValidator, MaxValueValidator
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


class AthleteInfo(models.Model):
    goals = models.TextField(null=True, blank=True)
    weight = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(899)
    ], null=True, blank=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
