import os
import time
from random import randint

from instagrapi import Client

ACCOUNT_ROOT_FILE_PATH = "account_data/"

def account_path(bot=None, username=""):
  return ACCOUNT_ROOT_FILE_PATH + f"{bot.username if bot else username}.json"


def get_update_user_stats(client: Client, bot=None, user=None):
      u_name = user.get("username") if user else bot.username

      try:
        u_info = client.user_info_by_username(u_name).dict()
        following = u_info.get("following_count")
        followers = u_info.get("follower_count")
        if bot:
          bot.following = following
          bot.followers = followers
          bot.save()
        else:
          return following, followers
      except Exception:
        client.relogin()
        client.dump_settings(account_path(bot))
        return


def login(client, bot):

    if os.path.isfile(account_path(bot)):
        print(f"Settings loaded for {bot.username}")
        client.load_settings(account_path(bot))
    
    client.set_locale("en_GB")
    client.set_country_code(44)
    client.set_timezone_offset(1 * 3600)


    client.login(username=bot.username, password=bot.password)
    get_update_user_stats(client=client, bot=bot)

    if not bot.ig_uid:
      bot.ig_uid = client.user_id
      bot.save()
    
    print(f"{bot.username} authenticated, beginning")

    if not os.path.isfile(account_path(bot)):
        print("Creating new settings for", bot.username)
        client.dump_settings(account_path(bot))
    

def unfollow_user(client, session, user_id, log=True):
      client.user_unfollow(user_id)
      session.unfollow_count += 1
      session.save()


def follow_user(client, session, user, lt_f=False):
    # When true, checks to make sure user following > followers
    if lt_f:
        following, followers = get_update_user_stats(client=client, user=user)

        if following <= followers:
            return

    client.user_follow(user.get("pk"))
    session.follow_count += 1
    session.save()


def dm_user(client, msg_count, user, msg="Hey!"):
    try:
        client.direct_send(msg, [user.get("pk")], [])
        msg_count += 1
    except Exception as e:
        print("Error DMing user ->", e)


def media_likers(client, post):
    try:
        likers = client.media_likers(post.get("id"))
        return likers
    except Exception as e:
        print("Error fetching likers on post", e)


def media_comment(client, session, post, comments):
      # rand = randint(0, len(comments - 1))
      # comment = comments[rand]

      client.media_comment(post.get("id"), comments[0], None)
      session.comment_count += 1

      session.save()


def media_like(client, session, post, comment=False, comment_freq=9, lb=30, ub=90):
        client.media_like(post.get("id"))
        session.like_count += 1

        if comment and session.like_count % comment_freq == 0:
            media_comment(client, session, post, ["🔥🔥🔥"])
        
        session.save()

        seconds = randint(lb, ub) / 10
        time.sleep(seconds)

