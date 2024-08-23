from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site


def send_confirmation_email(email, token_id, user_id):
    data = {
            'token_id':str(token_id),
            'user_id':str(user_id)
    }
    message = get_template('users/confirmation_email.txt').render(data)
    send_mail(subject='Please confirm email',
              message=message,
              from_email='hello@bodhiguru.com',
              recipient_list=[email],
              fail_silently=False)