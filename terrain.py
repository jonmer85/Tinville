import sys
import subprocess
import re
import os
from lettuce import *
from selenium import webdriver
from django.core.management import call_command
from django.core.management import execute_from_command_line
from unipath import Path

@before.harvest
def set_browser(step):
    desiredbrower = os.environ.get('lettucebrowser')
    if desiredbrower == 'Firefox':
        browser = webdriver.Firefox
    elif desiredbrower == 'Chrome':
        browser = webdriver.Chrome
    elif desiredbrower == 'Ie':
        browser = webdriver.Ie
    elif desiredbrower == 'Safari':
        browser = webdriver.Safari
    else:
        browser = webdriver.Firefox
    world.browser = browser()
    world.browser.implicitly_wait(10)  # seconds JON M TBD - Implicit wait not working on Chrome Driver :(

#@before.all
# Jon M - Commented this out since sync-ing the DB all the time was slow. Manually sync the test DB as needed with
# ./test syncdb as needed
def setup_database():
    call_command('syncdb', interactive=False, verbosity=0)

@before.each_scenario
def add_context_to_scenario(scenario):
    scenario.context = {}

@before.each_scenario
def clean_database(scenario):
    call_command('flush', noinitialdata=True, interactive=False, verbosity=0)
    call_command('loaddata', 'all.json', verbosity=0)

