from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

from carts.models import Cart

User = get_user_model()

STATUS_CHOICES = (
    ("Started", "Started"),
    ("Abandoned", "Abandoned"),
    ("Finish", "Finish"),
    )


class Oder(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    order_id = models.CharField(max_length=120, default='ABC', unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    sub_total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    tax_total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    final_total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Started")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.order_id