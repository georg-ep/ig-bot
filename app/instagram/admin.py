from django.contrib import admin
from instagram import models
from .textchoices import ClientStatus as CS
from celery import current_app as celery_app
from django.http import HttpResponseRedirect

# Register your models here.

@admin.register(models.AccountSwitchInterval)
class AccountSwitchIntervalAdmin(admin.ModelAdmin):
    list_display = ("id", "lower_limit", "higher_limit",)

@admin.register(models.Bot)
class BotAdmin(admin.ModelAdmin):
    change_form_template = "admin/client_changeform.html"
    list_display = (
        "username",
        "followers",
        "following",
        "ff_ratio",
        "last_finished",
        "daily_follows",
        "daily_unfollows",
    )

    def daily_follows(self, obj):
      return obj.daily_follow_count

    def daily_unfollows(self, obj):
      return obj.daily_unfollow_count
    

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}

        bot = models.Bot.objects.filter(id=object_id).first()
        extra_context["can_start_session"] = True
        extra_context["can_end_session"] = bot.status != CS.IDLE

        return super().change_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        if "_start" in request.POST:
            # Begin the instagram client
            celery_app.send_task("ig_session", kwargs={"bot_uid": obj.uid})
        if "_end" in request.POST:
            # Fetch list of active celery tasks, query and remove the active task
            i = celery_app.control.inspect()
            tasks = list(i.active().values())[0]
            for task in tasks:
                if task["kwargs"]["bot_uid"] == str(obj.uid):
                    celery_app.control.revoke(task["id"], terminate=True)
                    break
        return HttpResponseRedirect(".")


class SessionLimitInline(admin.TabularInline):
    model = models.SessionLimit
    extra = 0


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "bot",
        "session_type",
        "status",
    )
    inlines = [SessionLimitInline]


    def get_readonly_fields(self, request, obj):
        fields = [
            "comment_count",
            "like_count",
            "unfollow_count",
            "follow_count",
            "dm_count",
            "status",
        ]

        if not obj:
            return fields

        return super().get_fields(request)
