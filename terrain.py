from django.core.management import call_command
from lettuce import *
from selenium import webdriver

@before.harvest
def set_browser(step):
    world.browser = webdriver.Firefox()

@after.harvest
def foo(step):
    world.browser.quit()

@before.all
def setup_database():
    call_command('syncdb', interactive=False, verbosity=0)

@before.each_scenario
def clean_database(scenario):
    call_command('flush', interactive=False, verbosity=0)
