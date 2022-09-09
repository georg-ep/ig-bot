from django.core.management import BaseCommand
from instagrapi import Client
from instagram.models import Bot
from instagram.client import ig_actions as ig_a

class Command(BaseCommand):
    def handle(self, *args, **options):
      ig_client = Client()
      bot_uid = Bot.objects.filter(username="laughtv_uk").first().uid

      bot = Bot.objects.get(uid=bot_uid)

      ig_a.login(ig_client, bot)

      following = ig_client.user_following(ig_client.user_id)
      following = [user.dict() for user in following.values()] if len(following) else []
      
      followers = ig_client.user_followers(ig_client.user_id)
      followers = [user.dict() for user in followers.values()] if len(followers) else []

      print("following", len(following), "followers", len(followers))

      unfollow = []

      for follow in following:
        if not any(follower.get("pk") == follow.get("pk") for follower in followers):
            unfollow.append(follow)
            # TODO break loop on match unfollow with random count
      
      print(len(unfollow))
      
      # print()