from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    last_activity = models.DateTimeField(null=True)

    def update_last_activity(self):
        self.last_activity = timezone.now()
        self.save()
