from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField
from django.core.validators import RegexValidator
from .fields import AjaxCropImageField
from image_cropping import ImageRatioField, ImageCropField
# Create your models here.


class Shop(models.Model):
    user = models.ForeignKey('user.TinvilleUser')
    name = models.CharField(verbose_name="Shop name", unique=True, blank=False, null=False, db_index=True,
                            default=None, max_length=100)
    slug = models.SlugField()
    # banner = AjaxCropImageField(upload_to=lambda instance, filename: 'shops/{0}/banner/{1}'.format(instance.slug, filename),max_length=255)
    banner = ImageCropField(default='images/banner.jpg',
                               upload_to=lambda instance, filename: 'shops/{0}/banner/{1}'.format(instance.slug, filename),max_length=255)
    mobileBanner = ImageCropField(default='images/banner.jpg',
                               upload_to=lambda instance, filename: 'shops/{0}/banner/{1}'.format(instance.slug, filename),max_length=255)
    cropBanner = ImageRatioField('banner', '430x360')
    cropmobileBanner = ImageRatioField('mobileBanner', '430x360')


    logo = models.ImageField(upload_to=lambda instance, filename: 'shops/{0}/logo/{1}'.format(instance.slug, filename), max_length=255)
    aboutImg = models.ImageField(upload_to=lambda instance, filename: 'shops/{0}/aboutImg/{1}'.format(instance.slug, filename), max_length=255)
    aboutContent = HTMLField()
    color = models.CharField(default='#663399', max_length=7,
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
        self.slug = slugify(self.name.lower())
        super(Shop, self).save(*args, **kwargs)


SIZE_SET = "1"
SIZE_DIM = "2"
SIZE_NUM = "3"

SIZE_TYPES = [
    (SIZE_SET, "Set (eg. Small, Medium, Large)"),
    (SIZE_DIM, "Dimensions (eg. Length X Width)"),
    (SIZE_NUM, "Number (eg. Dress size)")
]


