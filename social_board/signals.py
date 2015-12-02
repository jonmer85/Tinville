from likes.signals import can_vote_test
from django.dispatch import receiver

def my_callback(sender, **kwargs):
    hi = 2

can_vote_test.connect(my_callback)

