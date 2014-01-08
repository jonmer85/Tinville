from django.core.management import call_command
from lettuce import before

@before.harvest
def setup_database(server):
    call_command('syncdb', interactive=False, verbosity=0)

@before.each_scenario
def clean_db(scenario):
    call_command('flush', interactive=False, verbosity=0)
