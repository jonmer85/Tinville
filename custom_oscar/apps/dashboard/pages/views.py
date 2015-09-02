from django.http import HttpResponseRedirect
from common.utils import is_url_taken_no_shop_check
from oscar.apps.dashboard.pages.views import PageUpdateView as CorePageUpdateView, PageCreateView as CorePageCreateView
from oscar.core.loading import get_model
from custom_oscar.apps.dashboard.pages import forms
from oscar.core.utils import slugify

FlatPage = get_model('flatpages', 'FlatPage')
Site = get_model('sites', 'Site')


class PageUpdateView(CorePageUpdateView):
    """
    View for updating flatpages from the dashboard.
    """
    form_class = forms.PageUpdateForm


class PageCreateView(CorePageCreateView):
    """
    View for updating flatpages from the dashboard.
    """
    form_class = forms.PageUpdateForm

    def form_valid(self, form):
        """
        Store new flatpage from form data. Checks wether a site
        is specified for the flatpage or sets the current site by
        default. Additionally, if URL is left blank, a slugified
        version of the title will be used as URL after checking
        if it is valid.
        """
        # if no URL is specified, generate from title
        page = form.save(commit=False)

        if not page.url:
            page.url = '/%s/' % slugify(page.title)

        if is_url_taken_no_shop_check(page.url):
            pass
        else:
            # use current site as default for new page
            page.save()
            page.sites.add(Site.objects.get_current())

            return HttpResponseRedirect(self.get_success_url(page))

        ctx = self.get_context_data()
        ctx['form'] = form
        return self.render_to_response(ctx)
