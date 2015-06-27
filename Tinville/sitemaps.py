from designer_shop.forms import Product
from designer_shop.models import Shop
from django.contrib import sitemaps
from django.core.urlresolvers import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home_about', 'home_faq', 'home', 'shoplist',
                'user.views.register']

    def location(self, item):
        return reverse(item)


class ShopsSitemap(sitemaps.Sitemap):
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        return Shop.objects.filter(user__is_approved = True)

    def location(self, item):
        return reverse('designer_shop.views.shopper', kwargs={'slug': item.slug})


class ItemsSitemap(sitemaps.Sitemap):
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return Product.objects.filter(structure="parent").filter(shop__user__is_approved = True)

    def location(self, item):
        return reverse('designer_shop.views.itemdetail', kwargs={'shop_slug': item.shop.slug, 'item_slug': item.slug})
