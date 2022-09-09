from django.core.management import BaseCommand
from instagrapi import Client
from instagram.models import Bot
from instagram.client import ig_actions as ig_a
from instagram.client.ig_scripts import run_next_session
from instagram.client import ig_scripts as ig

class Command(BaseCommand):
    def handle(self, *args, **options):
      ig_client = Client()
      bot_uid = Bot.objects.filter(username="goshopthemarket").first().uid

      bot = Bot.objects.get(uid=bot_uid)

      try:
        ig_a.login(ig_client, bot)
      except Exception:
        return run_next_session(bot)

      # cfg = {
      #     SessionTypes.LIKE_FOLLOW.value: ig.follow_like_bot,
      # }

      # cfg[bot.session_type](
      #     client=ig_client,
      #     tags="likeforlike",
      #     bot=bot,
      # )
      ig.follow_like_bot(client=ig_client, tags="likeforlike", bot=bot)