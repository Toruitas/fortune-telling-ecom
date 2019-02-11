import datetime
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField
from mezzanine.conf import settings
from celery.result import AsyncResult
from celery.task.control import revoke
# from celery.app.control import Control
# from django.conf import settings  # import setting module to get user
from .tasks import alert_membership_expiration_near_task, membership_expiration_annual_check_task


# Create your models here.


class MyProfile(models.Model):
    """
    Use this as proxy for user model?
    """
    def __str__(self):
        return str(self.user.username)

    user = models.OneToOneField("auth.User")  # (settings.AUTH_USER_MODEL) for custom auth model
    date_of_birth = models.DateTimeField(null=True, blank=True)
    phone = models.CharField(_("Phone number"),max_length=20)
    mobile_phone = models.CharField(_("Mobile phone number"),max_length=20,null=True, blank=True)
    shipping_detail_street = models.CharField(_("Street"), max_length=100,null=True, blank=True)
    shipping_detail_city = models.CharField(_("City"), max_length=100,null=True, blank=True)
    shipping_detail_state = models.CharField(_("State/Region"), max_length=100,null=True, blank=True)
    shipping_detail_postcode = models.CharField(_("Zip/Postcode"), max_length=10,null=True, blank=True)
    shipping_detail_country = models.CharField(_("Country"), max_length=100,null=True, blank=True)
    direction_1 = models.CharField(_("Direction of Primary Location"), max_length=100,default=("n", _("North")),
                                   choices=[("n", _("North")),
                                            ("nw", _("Northwest")),
                                            ("w", _("West")),
                                            ("sw", _("Southwest")),
                                            ("s", _("South")),
                                            ("se", _("Southeast")),
                                            ("e", _("East")),
                                            ("ne", _("Northeast")),
                                            ]
                                   )
    direction_2 = models.CharField(_("Direction of Secondary Location"),  max_length=100,default=("n", _("North")),
                                   choices=[("n", _("North")),
                                            ("nw", _("Northwest")),
                                            ("w", _("West")),
                                            ("sw", _("Southwest")),
                                            ("s", _("South")),
                                            ("se", _("Southeast")),
                                            ("e", _("East")),
                                            ("ne", _("Northeast")),
                                            ]
                                   )
    direction_3 = models.CharField(_("Direction of Third Location"), max_length=100,default=("n", _("North")),
                                   choices=[("n", _("North")),
                                            ("nw", _("Northwest")),
                                            ("w", _("West")),
                                            ("sw", _("Southwest")),
                                            ("s", _("South")),
                                            ("se", _("Southeast")),
                                            ("e", _("East")),
                                            ("ne", _("Northeast")),
                                            ]
                                   )


MEMBERSHIP_LEVELS = (
    ("regular", _("Regular")),
    ("gold",_("Gold")),
    ("diamond",_("Diamond"))
)


# class MembershipManager(models.Manager):


class Membership(models.Model):
    # http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add
    user = models.OneToOneField("auth.User")  # could do foreign key here...
    # always assoc w/ AUTH USER MODEL, don't import MyUser and go from there
    level = models.CharField(max_length=120, choices=MEMBERSHIP_LEVELS, default="regular")
    date_joined = models.DateTimeField(verbose_name='Joined Date', auto_now_add=True)
    date_start = models.DateTimeField(verbose_name='Start Date', blank=True, null=True)
    date_end = models.DateTimeField(verbose_name='End Date', blank=True, null=True)
    auto_renew = models.BooleanField(default=False)
    # http://stackoverflow.com/questions/22340258/django-list-field-in-model
    tasks = ArrayField(models.CharField(max_length=120),null=True, blank=True)

    # objects = MembershipManager()

    def __str__(self):
        return str(self.user.username + " level: " + self.level)

    @property
    def is_member(self):
        if self.level == "gold" or self.level == "diamond":
            return True
        else:
            return False

    def update_membership(self, next_level, years=1):
        """
        http://docs.celeryproject.org/en/latest/reference/celery.app.control.html
        http://docs.celeryproject.org/en/latest/userguide/workers.html
        Used when upgrading membership w/ next_levl in the payment process,
        :param next_level: change membership to this level
        :param years: if they order qty > 1
        :return:
        """
        # http://www.marinamele.com/2014/03/13-useful-tips-about-python-datetime.html
        # if premium, and user is renewing, should be from current date_end

        # cancel old tasks related to this user membership
        for id in self.tasks:
            try:
                task = AsyncResult(id)
                task.revoke()
            except:
                print("task not found")
        if next_level == "regular":  # if simple expiration, no need to mess with dates
            self.level = "regular"
        else:
            # If renewing
            if self.level == next_level:
                self.date_end = self.date_end + datetime.timedelta(days=366*years)
            # if upgrading
            elif self.level != next_level and next_level != "regular":
                self.date_start = timezone.now()
                self.date_end = self.date_start + datetime.timedelta(days=366*years)
                self.level = next_level
            # schedule event 1 year + 1 day in the future to downgrade membership if expired
            # save task id to obj, look it up, then resend
            check_task = membership_expiration_annual_check_task.apply_async(
                (self.id, self.user.id, self.date_end),
                eta=self.date_end + datetime.timedelta(days=1))
            # schedule event 1 year - 2 weeks in future to alert them about upcoming expiration
            alert_task = alert_membership_expiration_near_task.apply_async(
                (self.id, self.user.id, self.date_end),
                eta=self.date_end - datetime.timedelta(days=14))
            self.tasks = [check_task.id, alert_task.id]
        self.save()

    @property
    def get_membership(self):
        return self.level

    def expire_membership(self):
        """
        downgrades membership to regular if expired
        :return: True if downgraded, False if not
        """

        if self.date_end < timezone.now():  # if simple expiration
            self.date_start = timezone.now()
            self.date_end = self.date_start + datetime.timedelta(days=366000)  # 1000 years
            self.level = "regular"
            self.save()
            return True
        return False
