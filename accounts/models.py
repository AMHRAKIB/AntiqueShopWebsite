import stripe

from django.db import models
from django.conf import settings
from django.contrib.auth.signals import user_logged_in

# Create your models here.
stripe.api_key = settings.STRIPE_SECRET_KEY


class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120)

    def __unicode__(self):
        return str(self.stripe_id)


def get_or_create_stripe(sender, user, *args, **kwargs):
    try:
        user.userstripe.stripe_id
    except UserStripe.DoesNotExist:
        customer = stripe.Customer.create(
            email=str(user.email)
        )
        new_user_stripe = UserStripe.objects.create(
            user=user,
            stripe_id=customer.id
        )
    except:
        pass
    print(customer)


user_logged_in.connect(get_or_create_stripe)