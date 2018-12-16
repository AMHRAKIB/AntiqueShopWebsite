"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url

from orders.views import checkout, orders
from products.views import home, search, all, single

from carts.views import view, update_cart
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
                  re_path(r'^$', home, name='home'),
                  re_path(r'^s/$', search, name='search'),
                  re_path(r'^products/$', all, name='products'),
                  re_path(r'^products/(?P<slug>[\w-]+)/$', single, name='single_product'),
                  re_path(r'^cart/(?P<slug>[\w-]+)/$', update_cart, name='update_cart'),
                  re_path(r'^cart/$', view, name='cart'),
                  re_path(r'^checkout/$',checkout, name='checkout'),
                  re_path(r'^orders/$',orders, name='orders'),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.conf import settings
# from django.conf.urls import  include,url
# from django.conf.urls.static import static
# from django.contrib import admin
# admin.autodiscover()

# urlpatterns = [
#         url(r'^$','products.views.home',name='home'),
#         url(r'^s/$','products.views.search',name='search'),
#         url(r'^products/$','products.views.all', name='products'),
#         url(r'^products/(?P<slug>[\w-]+)/$', 'products.views.single', name='single_product'),
#         url(r'^cart/$','carts.views.view',name='cart'),

#         urlpath('admin/', include(admin.site.urls)),

#     ]
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
