from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
