import json
from django.views.generic import DetailView, TemplateView


class ProfileView(TemplateView):
    context_object_name = "social_profile"
    template_name = 'social_profile.html'


class CompetitionView(TemplateView):
    context_object_name = "social_competition"
    template_name = 'competition.html'


class CompetitionsView(TemplateView):
    context_object_name = "social_competitions"
    template_name = 'competitions.html'


class BrowseBoardsView(TemplateView):
    context_object_name = "browse_boards"
    template_name = 'browse_boards.html'



