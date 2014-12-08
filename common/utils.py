from django.conf import settings
from decimal import Decimal as D, ROUND_FLOOR

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

def get_designer_payout_amount(original_amount):
    # We take 10% of sales.
    return (original_amount -
            (original_amount * settings.TINVILLE_ORDER_SALES_CUT).quantize(D('0.01'), rounding=ROUND_FLOOR))

def isNoneOrEmptyOrWhitespace (validateString):
    if validateString:
        if validateString == ' ':
            return False
        else:
            return True
    return False