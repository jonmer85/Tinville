import logging
from django.contrib.sites.models import get_current_site
from oscar.core.loading import get_model, get_class
from Tinville.user.models import TinvilleUser

CommunicationEventType = get_model('customer', 'CommunicationEventType')
Dispatcher = get_class('customer.utils', 'Dispatcher')

logger = logging.getLogger('oscar.customer')


class SendOrderMixin(object):
    communication_type_code = 'ORDER_PLACED'

    def send_new_order_email(self, order):
        code = self.communication_type_code
        user = TinvilleUser.objects.get_by_natural_key('andrewfdabrowski@gmail.com')
        messages = CommunicationEventType.objects.get_and_render(
            code, self.get_message_context(user, order))
        if messages and messages['body']:
            Dispatcher().dispatch_user_messages(messages)

    def get_message_context(self, user, order):
        ctx = {
            'user': user,
            'order': order,

            'lines': order.lines.all()
        }

        #'site': get_current_site(self.request),

        return ctx