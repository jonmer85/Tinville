from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField
from django.core.validators import RegexValidator
# Create your models here.


class Shop(models.Model):
    user = models.ForeignKey('user.TinvilleUser')
    name = models.CharField(verbose_name="Shop name", unique=True, blank=False, null=False, db_index=True,
                            default=None, max_length=100)
    slug = models.SlugField()
    banner = models.ImageField(upload_to=settings.MEDIA_URL)
    logo = models.ImageField(upload_to=settings.MEDIA_URL)
    aboutContent = HTMLField()
    color = models.CharField(default='#ffffff', max_length=7,
        validators=[RegexValidator(
            regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
            message='Invalid hex code',
        ),]
    )



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
    image = models.ImageField(upload_to=settings.MEDIA_URL)
    price = models.DecimalField(max_digits=8, decimal_places=2)

SIZE_SET = "1"
SIZE_DIM = "2"
SIZE_NUM = "3"

SIZE_TYPES = [
    (SIZE_SET, "Set (eg. Small, Medium, Large)"),
    (SIZE_DIM, "Dimensions (eg. Length X Width)"),
    (SIZE_NUM, "Number (eg. Dress size)")
]


