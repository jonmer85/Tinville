import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, TemplateView, FormView, CreateView, ListView
from django.views.generic.edit import FormMixin
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from user.models import TinvilleUser
from .models import SocialCompetition,SocialBoard
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import *
from .utils import can_vote
from django.template import RequestContext
from likes.signals import can_vote_test


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

    can_vote_test.connect(can_vote)

    def get_context_data(self, **kwargs):
        context = super(BrowseBoardsView, self).get_context_data(**kwargs)
        context['social_boards'] = SocialBoard.objects.all()
        return context


class TrendingBoardView(TemplateView):
    context_object_name = "social_trending"
    template_name = 'trending_boards.html'


class SocialBoardCreateView(CreateView):
    context_object_name = "social_board_create"
    template_name = "create_board.html"
    form_class = SocialBoardForm
    success_url = '/social'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        social_used_image_form = SocialUsedImageFormSet(instance=request.user)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  social_used_image_form=social_used_image_form,
                                  # social_board_image_form=social_board_image_form
                                  ))

    def get_context_data(self, **kwargs):
        data = super(SocialBoardCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['usedsocialimages'] = SocialUsedImageFormSet(self.request.POST)
        else:
            data['usedsocialimages'] = SocialUsedImageFormSet()
        return data

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        social_used_image_form = SocialUsedImageFormSet(self.request.POST)
        if (form.is_valid() and social_used_image_form.is_valid()):
            return self.form_valid(form, social_used_image_form)
        else:
            return self.form_invalid(form, social_used_image_form)

    def form_valid(self, form, social_used_image_form):
        context = self.get_context_data()
        usedsocialimages = context['usedsocialimages']
        with transaction.commit_on_success():
            form.instance.user = self.request.user
            form.instance.updated_by = self.request.user
            self.object = form.save()
        if usedsocialimages.is_valid():
            usedsocialimages.instance = self.object
            usedsocialimages.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, social_used_image_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  social_used_image_form=social_used_image_form))


# class AddToCompetitionView(FormView):
#
# class RemoveFromCompetitionView(FormView):
#
# class SocialFollowView(FormView):
#
# class DeleteSocialBoardView(FormView)
