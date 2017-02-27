from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(TimeStampedModel, self).save(*args, **kargs)

    class Meta:
        abstract = True
