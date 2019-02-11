### custom command to create super user
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="sebadmin").exists():
            SUPERUSER_NAME = os.environ.get('SUPERUSER_NAME')  # "sebadmin"
            SUPERUSER_EMAIL = os.environ.get('SUPERUSER_EMAIL')  # "se.brilliant.aws@gmail.com"
            SUPERUSER_PW = os.environ.get('SUPERUSER_PW')  # "superbrilliant"
            User.objects.create_superuser(SUPERUSER_NAME, SUPERUSER_EMAIL, SUPERUSER_PW)
