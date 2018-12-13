from django.contrib import admin

# Register your models here.
from .models import Cart

class CartAdmin(admin.ModelAdmin):
	"""docstring for CartAmin"""
	class Meta:
		model = Cart


admin.site.register(Cart, CartAdmin)
