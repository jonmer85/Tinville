from lettuce import *
from selenium import webdriver
from django.core.management import call_command
from django.core.management import execute_from_command_line
import sys

currentbrowser =0
@before.harvest
def set_browser(step):
    browsers = {0: webdriver.Firefox,
                1: webdriver.Chrome,
                }

    world.browser = browsers[currentbrowser]()

@after.harvest
def foo(step):
    global currentbrowser
    world.browser.quit()
    if currentbrowser < 1:
        currentbrowser = currentbrowser + 1
        execute_from_command_line(sys.argv)

@before.all
def setup_database():
    call_command('syncdb', interactive=False, verbosity=0)

@before.each_scenario
def clean_database(scenario):
    call_command('flush', interactive=False, verbosity=0)
    call_command('loaddata', 'all.json', verbosity=0)
