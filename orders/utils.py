import string
import random

from .models import Oder


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    try:
        order = Oder.objects.get(order_id=the_id)
        id_generator()
    except Oder.DoesNotExist:
        return the_id
