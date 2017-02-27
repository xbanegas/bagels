from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from bagels.utils.models import TimeStampedModel
from bagels.users.models import User

class Tag(TimeStampedModel, MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __str__(self):
        return self.name
