from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from bagels.users.models import User

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255)
    tags = models.ManyToManyField('Tag')
    notes = models.TextField(blank=True)

    def __str__(self):
        rep = self.title if self.title else self.url
        return rep

class Tag(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __str__(self):
        return self.name
