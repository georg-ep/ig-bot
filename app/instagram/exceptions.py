from instagram.client.ig_scripts import run_next_session
from instagrapi.exceptions import (
    BadPassword, ReloginAttemptExceeded, ChallengeRequired,
    SelectContactPointRecoveryForm, RecaptchaChallengeForm,
    FeedbackRequired, PleaseWaitFewMinutes, LoginRequired
)
from instagram.client.ig_actions import account_path
import time
from .models import Session


def handle_exception(client, e):
    if isinstance(e, LoginRequired):
        session = Session.objects.filter(bot__username=client.username).first()
        if session.relogin_count > 1:
          return run_next_session(session.bot)
        print(client, e)
        print("Login Exception trying to relogin")
        client.relogin()
        session.relogin_count += 1
        session.save()
        time.sleep(5)
        client.dump_settings(account_path(username=client.username))

        print("dumped settings")
