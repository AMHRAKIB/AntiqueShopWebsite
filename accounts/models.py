import stripe
import random
import hashlib
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.core.mail import send_mail
# Create your models here.
stripe.api_key = settings.STRIPE_SECRET_KEY

User = get_user_model()


class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    def __unicode__(self):
        return str(self.stripe_id)


class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.confirmed)

    def activate_user_email(self):
        activation_url = "%s%s" %(settings.SITE_URL, reverse("activation_view", args = [self.activation_key]))
        context = {
            "activation_key":self.activation_key,
            "activation_url":activation_url,
            "user": self.user.username,
        }
        massage = render_to_string("accounts/activation_massage.txt",context)
        subject = "Please Activate your Email"
        self.email_user(subject,massage,settings.DEFAULT_FROM_EMAIL)

    def email_user(self,subject,massage,from_email=None, **kwargs):
        send_mail(subject,massage,from_email,[self.user.email], kwargs)



# def get_or_create_stripe(sender, user, *args, **kwargs):
#     try:
#         user.userstripe.stripe_id
#     except UserStripe.DoesNotExist:
#         customer = stripe.Customer.create(
#             email=str(user.email)
#         )
#         new_user_stripe = UserStripe.objects.create(
#             user=user,
#             stripe_id=customer.id
#         )
#     except:
#         pass


# user_logged_in.connect(get_or_create_stripe)

def get_create_stripe(user):
    new_user_stripe, created = UserStripe.objects.get_or_create(user=user)
    if created:
        customer = stripe.Customer.create(
            email=str(user.email)
        )
        new_user_stripe.stripe_id = customer.id
        new_user_stripe.save()


def user_created(sender, instance, created, *args, **kwargs):
    user = instance
    if created:
        get_create_stripe(user)
        email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user=user)
        if email_is_created:
            short_hash = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            base, domain = str(user.email).split("@")
            activation_key = hashlib.sha1((short_hash + base).encode('utf-8')).hexdigest()
            email_confirmed.activation_key = activation_key
            email_confirmed.save()
            email_confirmed.activate_user_email()

post_save.connect(user_created, sender=User)


