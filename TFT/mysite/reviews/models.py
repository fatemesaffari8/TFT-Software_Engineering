from django.db import models
from django.conf import settings

from centers.models import Center


class StarRating(models.Model):
    center_id = models.ForeignKey(Center, unique=False, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, unique=False, on_delete=models.DO_NOTHING)
    rate = models.IntegerField()
    class Meta:
        unique_together = (("center_id", "user_id"),)
