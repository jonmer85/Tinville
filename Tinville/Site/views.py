from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .models import MailingListItem
from .forms import MailingListItemForm


class CreateMailingListItemView(CreateView):
    model = MailingListItem
    success_url = reverse_lazy('home')
    form_class = MailingListItemForm
    template_name = 'teaser_home.html'

    def form_valid(self, form):
        ip = self.request.META.get("HTTP_X_FORWARDED_FOR", None)
        if ip:
            # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
            ip = ip.split(", ")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR", "")
        form.instance.ip_address = ip

        messages.success(self.request, "Thank for for signing up to our mailing list!")
        return super(CreateMailingListItemView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "This email address is already in our list or invalid")
        return super(CreateMailingListItemView, self).form_invalid(form)






