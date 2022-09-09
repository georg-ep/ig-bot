from django.core.management import BaseCommand
from user.models import User
from instagrapi import Client

class Command(BaseCommand):
    def handle(self, *args, **options):
      for user in User.objects.all():
          c = Client()
          c.login(user.username, user.password)
          
