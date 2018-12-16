from django.urls import reverse
import time
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from carts.models import Cart

from .models import Oder
from .utils import id_generator


def orders(request):
    context = {}
    template = "orders/user.html"
    return render(request, template, context)

@login_required
def checkout(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse("cart"))
    try:
        new_order = Oder.objects.get(cart=cart)
    except Oder.DoesNotExist:
        new_order = Oder()
        new_order.cart = cart
        new_order.user = request.user
        new_order.order_id = id_generator()
        new_order.save()
    except:
        return HttpResponseRedirect(reverse("cart"))
    if new_order.status == "Finish":
        del request.session['cart_id']
        del request.session['items_total']
    context = {}
    template = "products/home.html"
    return render(request, template, context)
