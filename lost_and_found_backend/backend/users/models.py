from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        LOSER = 'LOSER', 'Loser'
        OFFICE = 'OFFICE', 'Lost & Found Office'
        TECH = 'TECH', 'Technical Team'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.LOSER)

    def __str__(self):
        return f"{self.username} ({self.role})"
