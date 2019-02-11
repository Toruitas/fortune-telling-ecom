from celery import shared_task
from celery.utils.log import get_task_logger

from .utils import alert_membership_expiration_near, membership_expiration_annual_check

logger = get_task_logger(__name__)


@shared_task(name="alert_membership_expiration_near_task")
def alert_membership_expiration_near_task(membership_id, user_id, end_date):
    """
    Ends the user's membership after a year / on the date assigned
    http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
    Shared task for Django
    http://docs.celeryproject.org/en/stable/userguide/calling.html?highlight=eta#eta-and-countdown
    celery -A seb worker -l info
    celery help
    :param id:
    :param user_id:
    :param date:
    :return:
    """
    logger.info("Sent membership alert email")
    alert_membership_expiration_near(membership_id, user_id, end_date)


@shared_task(name="membership_expiration_annual_check_task")
def membership_expiration_annual_check_task(membership_id, user_id, end_date):
    """
    celery -A seb worker --loglevel=info
    :param user_id:
    :return:
    """
    membership_expiration_annual_check(membership_id, user_id, end_date)
    logger.info("Reduced membership to regular level")


# @shared_task(name="test_aws_revoke")
# def test_aws_revoke_task():
#     from django.conf import settings
#     from django.core.mail import EmailMessage
#     from django.template import Context
#     from django.template.loader import render_to_string
#
#     def send_feedback_email(email, message):
#         c = Context({'email': email, 'message': message})
#
#         email_subject = render_to_string(
#             'test/feedback_email_subject.txt', c).replace('\n', '')
#         email_body = render_to_string('test/feedback_email_body.txt', c)
#
#         email = EmailMessage(
#             email_subject, email_body, email,
#             [settings.DEFAULT_FROM_EMAIL], [],
#             headers={'Reply-To': email}
#         )
#         return email.send(fail_silently=False)
#
#     send_feedback_email("toruitas@gmail.com","not revoked")
#     print("not revoked")
#     logger.info("not revoked")