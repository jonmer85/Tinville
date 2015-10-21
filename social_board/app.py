from django.conf.urls import url
from oscar.core.loading import get_class
from oscar.core.application import Application

class SocialApplication(Application):
    name = 'social_board'
    profile_view = get_class('social_board.views', 'ProfileView')
    competition_view = get_class('social_board.views', 'CompetitionView')
    competitions_view = get_class('social_board.views', 'CompetitionsView')
    browse_boards_view = get_class('social_board.views', 'BrowseBoardsView')

    def get_urls(self):
        urlpatterns = super(SocialApplication, self).get_urls()
        urlpatterns += [
            url(r'^$', self.profile_view.as_view(), name='home'),
            url(r'^user/(?P<pk>\d+)/$',
                self.profile_view.as_view(), name='profile'),
            url(r'^competition/(?P<pk>\d+)/$',
                self.competition_view.as_view(), name='competition'),
            url(r'^competitions/$',
                self.competitions_view.as_view(), name='competitions'),
            url(r'^social_board/browse/$',
                self.browse_boards_view.as_view(), name='board_browse')]
        return self.post_process_urls(urlpatterns)

application = SocialApplication()