import urlparse
from django import forms
from django.core.exceptions import ValidationError
from django.core.urlresolvers import resolve
from common.utils import is_url_taken_no_shop_check
from oscar.apps.dashboard.pages.forms import PageUpdateForm as CorePageUpdateForm
from oscar.core.loading import get_model
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from oscar.core.validators import URLDoesNotExistValidator

FlatPage = get_model('flatpages', 'FlatPage')


class PageUpdateForm(CorePageUpdateForm):

    def clean_url(self):
        """
        Validate the input for field *url* checking if the specified
        URL already exists. If it is an actual update and the URL has
        not been changed, validation will be skipped.

        Returns cleaned URL or raises an exception.
        """
        url = self.cleaned_data['url']
        if 'url' in self.changed_data:
            if not url.endswith('/'):
                url += '/'
            if is_url_taken_no_shop_check(url):
                raise ValidationError(_('Specified page already exists!'), code='invalid')
        return url

    class Meta:
        model = FlatPage
        fields = ('title', 'url', 'content')
