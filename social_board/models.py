from django.db import models
from image_cropping import ImageRatioField
from django.conf import settings


class SocialBoard(models.Model):
    user = models.ForeignKey('user.TinvilleUser', verbose_name="User")
    date_created = models.DateTimeField("Competition Start Date")
    name = models.CharField('Name', max_length=128)
    description = models.TextField('Description', blank=True)
    is_deleted = models.BooleanField("Is Deleted", default=False)
    is_browsable = models.BooleanField("Is Browsable", default=True)

class SocialBoardImage(models.Model):
    user = models.ForeignKey('user.TinvilleUser', verbose_name="User")
    date_created = models.DateTimeField("Date Created", auto_now_add=True)
    original = models.ImageField("Original", upload_to=settings.SOCIAL_IMAGE_FOLDER, max_length=255)
    cropping = ImageRatioField('Cropping', '400x400', box_max_width=200)
    location = models.CharField('Location', max_length=10)
    is_deleted = models.BooleanField("Is Deleted", default=False)
    date_deleted = models.DateTimeField("Date Deleted", auto_now_add=True)

class SocialUsedImage(models.Model):
    image = models.ForeignKey('social_board.SocialBoardImage', verbose_name="Social Board Image")
    board = models.ForeignKey('social_board.SocialBoard', verbose_name="Social Board")
    date_used = models.DateTimeField("Date Created", auto_now_add=True)

class SocialVote(models.Model):
    user = models.ForeignKey('user.TinvilleUser', verbose_name="User")
    board = models.ForeignKey('social_board.SocialBoard', verbose_name="Social Board")
    competition = models.ForeignKey('social_board.SocialCompetition', verbose_name="Social Competition")
    date_created = models.DateTimeField("Date Created", auto_now_add=True)
    is_stale = models.BooleanField("Is Stale", default=False)

class SocialFollow(models.Model):
    following_user = models.ForeignKey('user.TinvilleUser', verbose_name="Following User", related_name="followees")
    followed_user = models.ForeignKey('user.TinvilleUser', verbose_name="Followed User", related_name="followers")
    date_followed = models.DateTimeField("Date Followed", auto_now_add=True)
    is_stale = models.BooleanField("Is Stale", default=False)

    @property
    def get_followers(self):
        return self.followers.all()

    @property
    def get_folowees(self):
        return self.followees.all()

class SocialCompetition(models.Model):
    name = models.CharField('Name', max_length=128)
    description = models.TextField('Description', blank=True)
    date_created = models.DateTimeField("Date Created", auto_now_add=True)
    date_competition_start = models.DateTimeField("Competition Start Date", blank=True, null=True)
    date_competition_end = models.DateTimeField("Competition End Date", blank=True, null=True)
    prize = models.CharField('Prize', max_length=128)
    is_active = models.BooleanField("Is Active", default=False)
    winner = models.ForeignKey('user.TinvilleUser', verbose_name="Winner", blank=True, null=True)

class SocialCompetitionsEntry(models.Model):
    board = models.ForeignKey('social_board.SocialBoard', verbose_name="Social Board")
    competition = models.ForeignKey('social_board.SocialCompetition', verbose_name="Social Competition", related_name='votes')

    @property
    def total_votes(self):
        return len(self.votes.filter(board=self.board, competition=self.competition))





