from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decouple import config


def send_confirmation_email(user, confirmation_url):
    subject = "Email Confirmation"
    message = render_to_string(
        "emails/confirmation_email.txt",
        {"user": user, "confirmation_url": confirmation_url},
    )
    from_email = config("EMAIL_USER")
    to = user.email

    send_mail(subject, message, from_email, [to])
