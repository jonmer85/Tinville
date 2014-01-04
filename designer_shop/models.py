from Tinville.settings.base import MEDIA_URL
from django.db import models

# Create your models here.


class Shop(models.Model):
    name = models.CharField(verbose_name="Shop name", unique=True, blank=False, null=False, db_index=True,
                            default=None, max_length=100)
    banner = models.ImageField(upload_to=MEDIA_URL)
    logo = models.ImageField(upload_to=MEDIA_URL)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/%s/" % self.name.replace(' ', '_')
