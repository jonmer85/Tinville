from django import forms
from .models import MailingListItem

class MailingListItemForm(forms.ModelForm):
    class Meta:
        model = MailingListItem

    def clean_email(self):
        """ Verifies that this email is not already in use """
        email = self.cleaned_data['email'].lower()  # Oh hey, this is important.
        return email

