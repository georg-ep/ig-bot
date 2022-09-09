from celery import shared_task
from instagrapi import Client

from instagram.client import ig_actions as ig_a
from instagram.client import ig_scripts as ig
from instagram.client.ig_scripts import run_next_session
from instagram.models import Bot
from instagram.handlers import challenge_code_handler
from instagram.exceptions import handle_exception


@shared_task(name="ig_session_check")
def ig_session_check_task():
    pass


@shared_task(name="ig_session")
def ig_session_task(bot_uid):
    ig_client = Client()

    ig_client.handle_exception = handle_exception

    bot = Bot.objects.get(uid=bot_uid)

    # try:
    ig_a.login(ig_client, bot)
    # except Exception:
    #   return run_next_session(bot)

    # cfg = {x
    #     SessionTypes.LIKE_FOLLOW.value: ig.follow_like_bot,
    # }

    # cfg[bot.session_type](
    #     client=ig_client,
    #     tags="likeforlike",
    #     bot=bot,
    # )
    ig.follow_like_bot(client=ig_client, tags="likeforlike", bot=bot)
