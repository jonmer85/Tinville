from Tinville.settings.base import MEDIA_URL
from django.db import models
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField

# Create your models here.


class Shop(models.Model):
    user = models.ForeignKey('user.TinvilleUser')
    name = models.CharField(verbose_name="Shop name", unique=True, blank=False, null=False, db_index=True,
                            default=None, max_length=100)
    slug = models.SlugField()
    banner = models.ImageField(upload_to=MEDIA_URL)
    logo = models.ImageField(upload_to=MEDIA_URL)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/%s/" % self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Shop, self).save(*args, **kwargs)

class Item(models.Model):
    shop = models.ForeignKey(Shop)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=MEDIA_URL)
    price = models.DecimalField(max_digits=8, decimal_places=2)

class RichTextField( models.Model ):
    
        aboutContent = HTMLField()
