from django.core.management import BaseCommand
from instagram.models import Session
from datetime import datetime
import pytz
from instagram.textchoices import SessionTypes, SessionStatus
from celery import current_app as celery_app
from instagrapi import Client
from instagram.client import ig_actions as ig_a
from instagram.client import ig_scripts as ig

def follow():
    print("following")


cfg = {
    SessionTypes.FOLLOW.value: follow,
}


class Command(BaseCommand):
    help = "View all active ig sessions"

    def handle(self, *args, **options):
        utc = pytz.timezone("Europe/London")
        now = utc.localize(datetime.now())

        # Active sessions
        a_s = Session.objects.all()
        a_s = a_s.filter(status=SessionStatus.NOT_STARTED)
        a_s = a_s.filter(start_time__lte=now, end_time__gt=now)

        # [
        #     celery_app.send_task("ig_session", kwargs={"session_uid": session.uid})
        #     for session in a_s
        # ]
        for session in a_s:
          client = Client()
          session = Session.objects.get(uid=session.uid)
          ig_a.login(client, session.client)
          ig.follow_like_bot(client, "followforfollow", session, 100)
