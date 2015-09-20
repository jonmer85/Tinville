from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django_bleach.models import BleachField
from django.core.validators import RegexValidator
# Create your models here.
from image_cropping import ImageRatioField, ImageCropField

def upload_to_about(instance, filename):
    return 'shops/{0}/aboutImg/{1}'.format(instance.slug, filename)

def upload_to_logo(instance, filename):
    return 'shops/{0}/logo/{1}'.format(instance.slug, filename)

def upload_to_mobile_banner(instance, filename):
    return 'shops/{0}/banner/{1}'.format(instance.slug, filename)

def upload_to_banner(instance, filename):
    return 'shops/{0}/banner/{1}'.format(instance.slug, filename)

class FeaturedShop(models.Model):
    featured = models.ForeignKey('designer_shop.Shop')


class Shop(models.Model):
    user = models.ForeignKey('user.TinvilleUser')
    name = models.CharField(verbose_name="Shop name", unique=True, blank=False, null=False, db_index=True,
                            default=None, max_length=100)
    slug = models.SlugField()
    banner = models.ImageField(default='images/banner.jpg',
                               upload_to=upload_to_banner, max_length=255)
    bannerCropping = ImageRatioField('banner', '1779x364', box_max_width=200)
    mobileBanner = models.ImageField(default='images/mobilebanner.jpg',
                               upload_to=upload_to_mobile_banner, max_length=255)
    mobileBannerCropping = ImageRatioField('mobileBanner', '968x642', box_max_width=200)

    logo = models.ImageField(upload_to=upload_to_logo, max_length=255)
    aboutImg = models.ImageField(upload_to=upload_to_about, max_length=255)
    # size is "width x height"
    aboutImgCropping = ImageRatioField('aboutImg', '155x155', box_max_width=200)
    aboutContent = BleachField()
    returnPolicy = BleachField(verbose_name="Return policy", blank=True, null=True)
    color = models.CharField(default='#5B595A', max_length=7,
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
ONE_SIZE = "4"

SIZE_TYPES = [
    (SIZE_SET, "Set (eg. Small, Medium, Large)"),
    (SIZE_DIM, "Dimensions (eg. Length X Width)"),
    (SIZE_NUM, "Number (eg. Dress size)"),
    (ONE_SIZE, "No Size/ One Size Fits All")
]
