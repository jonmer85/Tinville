from oscar.apps.checkout.session import CheckoutSessionMixin as CoreCheckoutSessionMixin

class CheckoutSessionMixin(CoreCheckoutSessionMixin):

    def get_context_data(self, **kwargs):
        # Use the proposed submission as template context data.  Flatten the
        # order kwargs so they are easily available too.
        ctx = self.build_submission(**kwargs)
        if self.template_name == 'gateway.html' and 'form' not in ctx:
            ctx['form'] = self.form_class()
        if self.template_name == 'gateway.html' and 'form2' not in ctx:
            ctx['form2'] = self.second_form_class()
        ctx.update(kwargs)
        ctx.update(ctx['order_kwargs'])
        return ctx