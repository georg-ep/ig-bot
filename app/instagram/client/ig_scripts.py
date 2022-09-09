import time
from datetime import datetime, timedelta
from random import randint

from celery import current_app as celery_app
from instagram.models import Bot, Session, AccountSwitchInterval
from instagram.textchoices import ClientStatus
from instagram.textchoices import SessionStatus as SS
from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes

from .ig_actions import account_path, follow_user, media_like, unfollow_user


def update_session(session, status: SS):
    session.status = status
    if status == SS.FINISHED:
        session.end_time = datetime.now()
    session.save()


def run_next_session(bot):

    available_bots = Bot.objects.exclude(id=bot.id).exclude(sessions__status=SS.RUNNING)

    session = bot.sessions.last()
    update_session(session, SS.FINISHED)

    bot.last_finished = datetime.now()
    bot.status = ClientStatus.IDLE
    bot.save()

    # Create delay for switching to the next account
    interval = AccountSwitchInterval.objects.get(id=1)
    sleep = randint(interval.lower_limit * 600, interval.higher_limit * 600) / 10
    eta = datetime.utcnow() + timedelta(seconds=sleep)



    # Restart current bot after random time if no other bots available
    if not available_bots.count():
        print(f"Only one client found -> sleeping for {sleep / 60} minutes")
        celery_app.send_task("ig_session", kwargs={"bot_uid": bot.uid}, eta=eta)
        return

    print(f"Bots available: {available_bots.count()}")
    bot = available_bots.order_by("last_finished").last()
    print(f"Next bot to run: {bot.username} -> in {sleep / 60} mins")
    celery_app.send_task("ig_session", kwargs={"bot_uid": bot.uid}, eta=eta)


def follow_like_bot(client, tags, bot: Bot):

    bot_can_run = bot.can_follow or bot.can_unfollow
    session = Session.objects.create(bot=bot) if bot_can_run else None
    posts_from_tags = None


    posts_from_tags = randint(15, 40)
    post_raw = client.hashtag_medias_recent_v1(tags, amount=posts_from_tags)

    update_session(session, SS.RUNNING)
    bot.status = ClientStatus.FOLLOWING
    bot.save()
    posts = [post.dict() for post in post_raw]

    print(f"Interacting with {posts_from_tags} posts")

    for index, post in enumerate(posts):
        rand = randint(1, 2)
        print(f"{index + 1} / {posts_from_tags}")

        user_medias_raw = client.user_medias(post["user"]["pk"], rand)
        user_medias = [media.dict() for media in user_medias_raw]

        for media in user_medias:
            media_like(client, session, media, comment=True, lb=1, ub=4)

        if bot.can_follow:
          follow_user(client, session, post["user"], lt_f=True)

        seconds = randint(20, 40) / 10
        time.sleep(seconds)

    if bot.can_unfollow:
      unfollow_not_following(client, session, posts_from_tags)

    run_next_session(bot)

def unfollow_not_following(client, session, posts_from_tags):

    lb = 10
    ub = 30

    if session.bot.following > session.bot.followers and posts_from_tags:
        lb = posts_from_tags
        ub = lb + randint(5, 10)

    rand = randint(lb, ub)
    unfollowed = 0


    following = client.user_following(client.user_id, session.bot.following)
    following = [user_id for user_id in following.keys()] if len(following) else []

    followers = client.user_followers(client.user_id, session.bot.followers)
    followers = [user_id for user_id in followers.keys()] if len(followers) else []

    print(f"Unfollowing {rand} users")
    print(f"{session.bot.username}: Following {len(following)}, Followers {len(followers)}")

    session.bot.status = ClientStatus.UNFOLLOWING
    session.bot.save()

    for follow in following:
        if not any(follower == follow for follower in followers):

            unfollow_user(client, session, follow)
            unfollowed += 1
            print(f"Unfollowed: {unfollowed}/{rand}")

            seconds = randint(20, 50) / 10
            time.sleep(seconds)

            if unfollowed == rand or session.bot.following < 200 and session.bot.following <= session.bot.followers:
                break
