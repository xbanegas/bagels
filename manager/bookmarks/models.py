from django.db import models

from bagels.utils.models import TimeStampedModel
from bagels.users.models import User

class Bookmark(TimeStampedModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255)
    tags = models.ManyToManyField('Tag', blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        rep = self.title if self.title else self.url
        return rep

