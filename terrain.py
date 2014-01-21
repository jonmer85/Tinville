from django.core.management import call_command
from lettuce import before

@before.all
def setup_database():
    call_command('syncdb', interactive=False, verbosity=0)

@before.each_scenario
def clean_db(scenario):
    call_command('flush', interactive=False, verbosity=0)
