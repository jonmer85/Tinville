import urlparse
from django.conf import settings
import lettuce
from lettuce.django.server import ThreadedServer, DefaultServer


class DefaultSecureServer(DefaultServer):
    """A silenced, lightweight and simple django's builtin server so
    that lettuce can be used with selenium, webdriver, windmill or any
    browser tool"""

    def __init__(self, *args, **kwargs):
        super(DefaultSecureServer, self).__init__(*args, **kwargs)

        # queue = create_mail_queue()
        # self._server = ThreadedServer(self.address, self.port, queue)

    # def start(self):
    #     super(DefaultServer, self).start()
    #
    #     if self._server.should_serve_admin_media():
    #         msg = "Preparing to serve django's admin site static files"
    #         if getattr(settings, 'LETTUCE_SERVE_ADMIN_MEDIA', False):
    #             msg += ' (as per settings.LETTUCE_SERVE_ADMIN_MEDIA=True)'
    #
    #         print "%s..." % msg
    #
    #     self._server.start()
    #     self._server.wait()
    #
    #     addrport = self.address, self._server.port
    #     if not self._server.is_alive():
    #         raise LettuceServerException(
    #             'Lettuce could not run the builtin Django server at %s:%d"\n'
    #             'maybe you forgot a "runserver" instance running ?\n\n'
    #             'well if you really do not want lettuce to run the server '
    #             'for you, then just run:\n\n'
    #             'python manage.py --no-server' % addrport,
    #         )
    #
    #     print "Django's builtin server is running at %s:%d" % addrport
    #
    # def stop(self, fail=False):
    #     pid = self._server.pid
    #     if pid:
    #         os.kill(pid, 9)
    #
    #     super(DefaultServer, self).stop()
    #
    #     code = int(fail)
    #     return sys.exit(code)

    def url(self, url=""):
        base_url = "https://%s" % ThreadedServer.get_real_address(self.address)

        # if self.port is not 80:
        #     base_url += ':%d' % self.port

        return urlparse.urljoin(base_url, url)

def get_server():
    return lettuce.django.get_server(address=settings.TEST_SERVER_ADDRESS)
