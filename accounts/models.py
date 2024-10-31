from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    # Add any additional fields you need here
    last_active_datetime = models.DateTimeField(default=timezone.now)

    def update_last_activity(self):
        self.last_activity = timezone.now()
        self.save()