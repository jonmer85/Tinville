import datetime
from user.models import TinvilleUser

class PromoterMiddleware(object):

    def process_request(self, request):
        if 'promoter_created' in request.session and 'promoter' in request.session:
            expired = datetime.datetime.now() - request.session['promoter_created']
            if expired.total_seconds() > 86400:
                del request.session['promoter_created']
                del request.session['promoter']

        if 'promoter' in request.GET:
            if 'promoter' not in request.session:
                promoter_id = request.GET.get('promoter', '')
                promoter = TinvilleUser.objects.get(promoter_code=promoter_id)
                request.session['promoter'] = promoter
                request.session['promoter_created'] = datetime.datetime.now()
