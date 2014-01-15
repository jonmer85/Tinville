
from django.db import models

# Create your models here.


class MailingListItem(models.Model):
    email = models.EmailField(verbose_name='email address', unique=True, db_index=True, max_length=254)
    ip_address = models.GenericIPAddressField(blank=True, null=True, editable=False)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.email