import json
from django.views.generic import DetailView, TemplateView, FormView, CreateView, ListView
from django.views.generic.edit import FormMixin
from django.db import transaction
from user.models import TinvilleUser
from .models import SocialCompetition,SocialBoard
from .forms import *


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


class BrowseBoardsView(FormMixin, TemplateView):
    context_object_name = "browse_boards"
    template_name = 'browse_boards.html'
    form_class = SocialInteractionForm

    def get_context_data(self, **kwargs):
        context = super(BrowseBoardsView, self).get_context_data(**kwargs)
        context['social_boards'] = SocialBoard.objects.filter(user=self.request.user)
        context['form'] = self.get_form(SocialInteractionForm)
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


class SocialInteractionView(FormView):
    context_object_name = "social_board_create"
    template_name = "view_board.html"
    form_class = SocialInteractionForm
    success_url = '/social'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        social_comment_form = SocialUsedImageFormSet(instance=request.social_board)
        social_vote_form = SocialVoteFormset(instance=request.social_board)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  social_comment_form=social_comment_form,
                                  social_vote_form=social_vote_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        social_used_image_form = SocialUsedImageFormSet(self.request.POST)
        if (form.is_valid() and social_used_image_form.is_valid()):
            return self.form_valid(request, form, social_used_image_form)
        else:
            return self.form_invalid(form, social_used_image_form)

    def form_valid(self, request, form, social_used_image_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        social_board = form.save(commit=False)
        social_board.user = request.user
        self.object = social_board.save()
        social_used_image_form.instance = self.object
        social_used_image_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, social_used_image_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  social_used_image_form=social_used_image_form))




# class AddToCompetitionView(FormView):
#
# class RemoveFromCompetitionView(FormView):
#
# class SocialVoteView(FormView):
#
# class SocialFollowView(FormView):

# class DeleteSocialBoardView(FormView)
