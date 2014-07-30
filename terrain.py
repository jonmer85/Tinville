import sys
import subprocess
import re

from lettuce import *
from selenium import webdriver
from django.core.management import call_command
from django.core.management import execute_from_command_line
from unipath import Path



currentbrowser =0
@before.harvest
def set_browser(step):
    browsers = (webdriver.Firefox,
                webdriver.Chrome,
                )

    world.browser = browsers[currentbrowser]()
    world.browser.implicitly_wait(10)  # seconds JON M TBD - Implicit wait not working on Chrome Driver :(

@after.harvest
def foo(step):
    global currentbrowser
    world.browser.quit()
    if currentbrowser < 1:
        currentbrowser = currentbrowser + 1
        execute_from_command_line(sys.argv)

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
    pythonexe = re.sub(r'python.*', 'activate', sys.executable)
    projectdir = Path(__file__).ancestor(1)
    subprocess.call('. ' + pythonexe + ' ; cd ' + projectdir + ' ; (./test sqlflush | ./test dbshell)', shell=True)
    # subprocess.call('. ' + pythonexe + ' ; cd ' + projectdir + ' ; (./test collectmedia --noinput)', shell=True)
    call_command('loaddata', 'all.json', verbosity=0)

