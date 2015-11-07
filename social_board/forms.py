from django.forms.models import modelformset_factory, BaseModelFormSet
from django import forms
from django.forms.models import inlineformset_factory
from oscar.core.loading import get_class, get_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Fieldset, HTML, Button, Hidden
from crispy_forms.bootstrap import PrependedText, Accordion, AccordionGroup

SocialBoard = get_model('social_board', 'SocialBoard')
SocialComment = get_model('social_board', 'SocialComment')
SocialVote = get_model('social_board', 'SocialVote')
SocialBoardImage = get_model('social_board', 'SocialBoardImage')
SocialUsedImage = get_model('social_board', 'SocialUsedImage')


class SocialBoardForm(forms.ModelForm):
    class Meta:
        model = SocialBoard
        exclude = ('is_deleted','user')


class SocialUsedImageForm(forms.ModelForm):
    class Meta:
        model = SocialUsedImage


BaseSocialUsedImageFormSet = inlineformset_factory(
    SocialBoard, SocialUsedImage, form=SocialUsedImageForm, fields=('cropping', 'location', 'image'), min_num=1, max_num=4)

class SocialUsedImageFormSet(BaseSocialUsedImageFormSet):
    def __init__(self, *args, **kwargs):
        super(SocialUsedImageFormSet, self).__init__(*args, **kwargs)





class SocialInteractionForm(forms.ModelForm):
    class Meta:
        model = SocialBoard
        exclude = ('is_deleted', 'user', 'description', 'name', 'is_browsable')


BaseSocialCommentFormset = inlineformset_factory(
    SocialBoard, SocialComment, form=SocialInteractionForm, fields=('comment',), min_num=1, max_num=1)

class SocialCommentFormSet(BaseSocialCommentFormset):
    def __init__(self, *args, **kwargs):
        super(SocialCommentFormSet, self).__init__(*args, **kwargs)


class SocialImageAddForm(forms.ModelForm):
    class Meta:
        model = SocialBoardImage
        exclude = ('user', 'date_created', 'is_deleted', 'date_deleted',)

