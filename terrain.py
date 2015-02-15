import sys
import subprocess
import re
import os
from lettuce import *
from selenium import webdriver
from django.core.management import call_command
from Tinville.settings.base import PROJECT_DIR
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


#@before.all
# Jon M - Commented this out since sync-ing the DB all the time was slow. Manually sync the test DB as needed with
# ./test syncdb as needed
def setup_database():
    call_command('migrate', interactive=False, verbosity=0)

@before.each_scenario
def add_context_to_scenario(scenario):
    scenario.context = {}

@before.each_scenario
def clean_database(scenario):
    call_command('flush', noinitialdata=True, interactive=False, verbosity=0)
    subprocess.call('. ' + sys.executable.replace('python2.7', 'activate') + '; cd ' + PROJECT_DIR[:-8] +
                    ' ; (./lettuce_tests collectmedia --noinput -v 0 > /dev/null)', shell=True)
    # call_command('collectmedia', noinitialdata=True, interactive=False, verbosity=0)
    call_command('loaddata', 'all.json', verbosity=0)
    call_command('loaddata', 'initial_data2.json', verbosity=0)

@before.each_scenario
def clear_cookies(scenario):
    world.browser.delete_all_cookies()