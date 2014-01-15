from django import forms
from .models import MailingListItem

class MailingListItemForm(forms.ModelForm):
    class Meta:
        model = MailingListItem

