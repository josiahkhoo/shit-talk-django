from django.db import models
from django.utils import timezone

# Create your models here.


class Chatroom(models.Model):
    name = models.CharField(max_length=30)
    key = models.CharField(max_length=10)
    datetime_created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
