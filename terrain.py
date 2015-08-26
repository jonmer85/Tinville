import sys
import subprocess
import re
import os
from django.conf import settings
from lettuce import *
from selenium import webdriver
from django.core.management import call_command
from Tinville.settings.base import PROJECT_DIR
from user.models import TinvilleUser


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
    if settings.LETTUCE_RUN_ON_HEROKU:
        call_command('flush', noinitialdata=True, interactive=False, settings='Tinville.settings.lettuce_tests_heroku')
        call_command('loaddata', 'all.json', settings='Tinville.settings.lettuce_tests_heroku')
        call_command('loaddata', 'initial_data2.json', settings='Tinville.settings.lettuce_tests_heroku')
        # execute('heroku run ./lettuce_tests_heroku compress --force --app tinville-lettuce')
    else:
        call_command('flush', noinitialdata=True, interactive=False)
        call_command('collectmedia', interactive=False)
        call_command('loaddata', 'all.json', verbosity=0)
        call_command('loaddata', 'initial_data2.json', verbosity=0)
        # call_command('compress', force=True, interactive=False)

    demo_user = TinvilleUser.objects.get(email='demo@user.com')
    demo_user.is_approved = True
    demo_user.save()

def execute(command):
    with open('test.log', 'w') as f:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        for c in iter(lambda: process.stdout.read(1), ''):
            sys.stdout.write(c)
            f.write(c)


@before.each_scenario
def clear_cookies(scenario):
    world.browser.delete_all_cookies()

@before.each_scenario
def add_context_to_scenario(scenario):
    scenario.context = {}

@after.each_scenario
def clear_context(scenario):
    scenario.context.clear()