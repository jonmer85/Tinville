import logging
from django.contrib.sites.models import get_current_site
from oscar.core.loading import get_model, get_class
from user.models import TinvilleUser
from common.utils import ExtractDesignerIdFromOrderId

CommunicationEventType = get_model('customer', 'CommunicationEventType')
Dispatcher = get_class('customer.utils', 'Dispatcher')
Order = get_model('order', 'Order')

logger = logging.getLogger('oscar.checkout')


class SendOrderMixin(object):
    communication_type_code = 'DESIGNER_ORDER_PLACED'

    def send_new_order_email(self, top_level_order):
        code = self.communication_type_code

        orders = Order.objects.filter(number__contains="-"+str(top_level_order.number))
        for order in orders:
            designerId = ExtractDesignerIdFromOrderId(order.number)
            user = TinvilleUser.objects.get(id=designerId)
            #Loads DESIGNER_ORDER_PLACED from DB fixture
            messages = CommunicationEventType.objects.get_and_render(
                code, self.get_message_context(user, order))

            if messages and messages['body']:
                dispatcher = Dispatcher(logger)
                dispatcher.dispatch_user_messages(user, messages)

    def get_message_context(self, user, order):
        ctx = {
            'user': user,
            'order': order,
            'lines': order.lines.all()
        }

        return ctx