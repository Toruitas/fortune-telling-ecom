from datetime import datetime
from django.conf import settings  # import setting module to get user
from django.db import models


class Fortune(models.Model):
    """
    user: user object
    birthday: of user. Since a user could be doing it for someone else, don't get this from user obj
    date: processed on which date
    content: what the fortune says
    image: lucky sign?
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE)
    birthday = models.DateTimeField(blank=False, null=False)
    date = models.DateTimeField(blank=False, null=False, default=datetime.now)
    # content
    # image