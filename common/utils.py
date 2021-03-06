import urlparse
from crispy_forms.layout import Layout, Field, Div, HTML
from django.conf import settings
from decimal import Decimal as D, ROUND_FLOOR
import string
from django.core.exceptions import ValidationError, SuspiciousOperation
import re
from django.core.urlresolvers import resolve
from designer_shop.models import Shop

def convert_to_currency(orignal_amount):
    return '{:,.2f}'.format(orignal_amount)

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

def get_list_or_empty(model, **kwargs):
    try:
        return list(model.objects.filter(**kwargs))
    except model.DoesNotExist:
        return []

def get_dict_value_or_validation_error(dict, key):
    if key in dict:
        return dict[key]
    else:
        raise ValidationError('No key %s in %s' % (key, dict))

def get_dict_value_or_suspicious_operation(dict, key):
    if key in dict:
        return dict[key]
    else:
        raise SuspiciousOperation('No key %s in %s' % (key, dict))

def get_designer_payout_amount(original_amount):
    # We take 20% of sales.
    return (original_amount -
            (original_amount * settings.TINVILLE_ORDER_SALES_CUT).quantize(D('0.01'), rounding=ROUND_FLOOR))

def get_promoter_payout_amount(original_amount):
    return(original_amount * settings.TINVILLE_PROMOTER_SALES_CUT).quantize(D('0.01'), rounding=ROUND_FLOOR)

def isNoneOrEmptyOrWhitespace (validateString):
    if validateString:
        if validateString.isspace():
            return False
        else:
            return True
    return False
def CroppedFieldLayout(croppedField, preview):
    return \
        Layout(
            Field(croppedField, css_class='hidden'),
            HTML(str.format("""
                    <div class="docs-toolbar hidden">
                      <div class="btn-group">
                        <button class="btn btn-primary" data-method="zoom" data-option="0.1" type="button" title="Zoom In" onclick="$('#{0}').cropper(&quot;zoom&quot;, 0.1)">
                            <span class="glyphicon glyphicon-zoom-in"></span>
                        </button>
                        <button class="btn btn-primary" data-method="zoom" data-option="-0.1" type="button" title="Zoom Out" onclick="$('#{0}').cropper(&quot;zoom&quot;, -0.1)">
                            <span class="glyphicon glyphicon-zoom-out"></span>
                        </button>
                        <button class="btn btn-primary" data-method="rotate" data-option="-90" type="button" title="Rotate Left" onclick="$('#{0}').cropper(&quot;rotate&quot;, -90)">
                            <span class="glyphicon glyphicon-share-alt gly-flip-horizontal"></span>
                        </button>
                        <button class="btn btn-primary" data-method="rotate" data-option="90" type="button" title="Rotate Right" onclick="$('#{0}').cropper(&quot;rotate&quot;, 90)">
                            <span class="glyphicon glyphicon-share-alt"></span>
                        </button>
                      </div>
                    </div>""", preview)),
            Div(
                HTML(str.format("<img id='{0}'></img>", preview)),
                css_class='img-container', style="margin-top: 5px; margin-bottom: 10px"
            )
        )

def is_url_taken_no_shop_check(url):
    if resolve(url).view_name != 'designer_shop.views.shopper':
        return True
    return False


def ExtractDesignerIdFromOrderId(orderId):
    shopIdMatch = re.search('^([0-9]+)', orderId)
    shopId = shopIdMatch.group()
    shop = Shop.objects.get(pk=shopId)
    designerId = shop.user.id
    return designerId

def get_top_level_order_number(designer_order_number):
    return designer_order_number[designer_order_number.find("-")+1:]


from functools import wraps
from django.views.decorators.cache import cache_page
from django.utils.decorators import available_attrs

def passes_test_cache(test_func, timeout=None, using=None, key_prefix=None):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request):
                return cache_page(timeout, cache=using, key_prefix=key_prefix)(view_func)(request, *args, **kwargs)
            else:
                return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
