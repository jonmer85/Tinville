from common.test_utils import create_in_transit_event
from django.contrib import admin
from oscar.core.loading import get_model

from oscar.apps.order.admin import *  # noqa

ShippingEvent = get_model('order', 'ShippingEvent')
ShippingEventQuantity = get_model('order', 'ShippingEventQuantity')

class ShippingEventLineInline(admin.TabularInline):
    model = ShippingEventQuantity
    extra = 0

class ShippingEventAdmin(admin.ModelAdmin):

    actions = ['simulate_intransit_event']

    inlines = [ShippingEventLineInline]

    def simulate_intransit_event(self, request, queryset):
        updates = 0
        for event in queryset:
            if event.event_type.code == 'shipped':
                create_in_transit_event(event.order.number, event.group, event.lines)
                updates += 1

        if updates == 1:
            message_bit = "1 shipping 'in transit' event was"
        else:
            message_bit = "%s shipping 'in transit' events were" % updates
        self.message_user(request, "%s successfully created." % message_bit)

    simulate_intransit_event.short_description = "Test Only: Create simulated in transit event for shipped event"



admin.site.unregister(ShippingEvent)
admin.site.register(ShippingEvent, ShippingEventAdmin)

