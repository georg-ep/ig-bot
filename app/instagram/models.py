from datetime import datetime
from multiprocessing.connection import Client
from django.db import models
import uuid
from .textchoices import SessionTypes, SessionStatus, ClientStatus
from django.db.models import Sum
# Create your models here.

class AccountSwitchInterval(models.Model):
    lower_limit = models.PositiveSmallIntegerField(default=0)
    higher_limit = models.PositiveSmallIntegerField(default=0)


class Bot(models.Model):
    uid = models.UUIDField(
        editable=False,
        default=uuid.uuid4,
    )
    name = models.CharField(
        default="",
        max_length=255,
        null=True,
        blank=True,
    )
    username = models.CharField(
        unique=True,
        max_length=255,
    )
    password = models.CharField(
        max_length=255,
    )
    following = models.PositiveIntegerField(default=0, null=True, blank=True)
    followers = models.PositiveIntegerField(default=0, null=True, blank=True)
    ig_uid = models.PositiveBigIntegerField(default=None, null=True, blank=True)
    last_finished = models.DateTimeField(
        null=True,
        blank=True,
        auto_now_add=True,
    )
    status = models.CharField(
        default=ClientStatus.IDLE,
        choices=ClientStatus.choices,
        max_length=255,
    )

    @property
    def ff_ratio(self):
      following, followers = self.following, self.followers
      return following / followers if following != 0 and followers != 0 else 0
    
    @property
    def daily_sessions(self):
      today = datetime.utcnow().date()
      start = datetime(today.year, today.month, today.day, 0, 0)
      end = datetime(today.year, today.month, today.day + 1, 0, 0)
      sessions = Session.objects.filter(start_time__gte=start, end_time__lte=end, bot=self)
      return sessions

    
    @property
    def daily_follow_count(self):
      sessions = self.daily_sessions
      return sessions.aggregate(follows=Sum("follow_count"))["follows"]

    @property
    def daily_unfollow_count(self):
      sessions = self.daily_sessions
      return sessions.aggregate(unfollows=Sum("unfollow_count"))["unfollows"]

    @property
    def can_follow(self):
      new_account = self.followers + 50 > self.following and self.followers < 200
      old_account = self.followers > 200 and self.following < self.followers 
      return True if new_account or old_account else False 
    
    @property
    def can_unfollow(self):
      is_experienced_account = self.followers > 200 and self.ff_ratio > 1
      is_following_cap = self.following > self.followers + 100
      return True if is_experienced_account or is_following_cap else False

    def __str__(self):
        return self.username

class BotFollow(models.Model):
    user_id = models.BigIntegerField()
    time = models.DateTimeField(auto_now_add=True, editable=False)

class Session(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(null=True, blank=True)
    like_count = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
    )
    follow_count = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
    )
    unfollow_count = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
    )
    comment_count = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
    )
    dm_count = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
    )
    session_type = models.CharField(
        default=SessionTypes.LIKE_FOLLOW,
        choices=SessionTypes.choices,
        max_length=255,
    )
    status = models.CharField(
        default=SessionStatus.RUNNING,
        choices=SessionStatus.choices,
        max_length=255,
    )

    @property
    def actions(self):
        return (
            self.comment_count
            + self.dm_count
            + self.like_count
            + self.unfollow_count
            + self.follow_count
        )
        

    def __str__(self):
        return self.bot.username + " : " + self.session_type + " : " + self.status


class SessionLimit(models.Model):
    like_count = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
    )
    follow_count = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
    )
    unfollow_count = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
    )
    comment_count = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
    )
    relogin_count = models.PositiveSmallIntegerField(default=0)
    dm_count = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
    )
    session = models.OneToOneField(
        Session,
        on_delete=models.CASCADE,
        related_name="limits",
        null=True,
        blank=True,
    )
