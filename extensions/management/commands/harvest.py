import os
from lettuce.django.management.commands.harvest import Command as Harvest
from optparse import make_option


class Command(Harvest):
    option_list = Harvest.option_list + (
             make_option('-B', '--browser', type='str', dest="browser", default="Firefox",
             help="the browser that the lettuce tests will run against"),
    )

    def handle(self, *args, **options):
        self.browser = options.get("browser")
        os.environ["lettucebrowser"] = self.browser
        super(Command, self).handle(*args, **options)