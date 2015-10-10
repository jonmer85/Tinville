from oscar.apps.voucher.abstract_models import AbstractVoucher as CoreAbstractVoucher

from django.db import models

class Voucher(CoreAbstractVoucher):
    is_tinville_voucher = models.BooleanField(default=False)

from oscar.apps.voucher.models import *