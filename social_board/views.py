import json
from django.views.generic import DetailView, TemplateView
from user.models import TinvilleUser
from .models import SocialCompetition


class ProfileView(DetailView):
    context_object_name = "social_profile"
    template_name = 'social_profile.html'
    model = TinvilleUser


class CompetitionView(DetailView):
    context_object_name = "social_competition"
    template_name = 'competition.html'
    model = SocialCompetition


class CompetitionsView(TemplateView):
    context_object_name = "social_competitions"
    template_name = 'competitions.html'


class BrowseBoardsView(TemplateView):
    context_object_name = "browse_boards"
    template_name = 'browse_boards.html'



