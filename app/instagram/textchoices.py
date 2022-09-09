from django.db import models

class SessionTypes(models.TextChoices):
    LIKE_FOLLOW = "Like Follow"

class SessionStatus(models.TextChoices):
    RUNNING = "Running"
    FINISHED = "Finished"
    ERROR = "Error"

class ClientStatus(models.TextChoices):
    FOLLOWING = "Following"
    UNFOLLOWING = "Unfollowing"
    IDLE = "Idle"
