from django.conf.urls import url, include
from rest_framework_mongoengine import routers

from . import views
from . import serializers

router = routers.DefaultRouter()
router.register(r'restaurants', serializers.restaurantsViewSet, r"restaurants")

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^listar/$', views.listar, name='listar'),
  url(r'^add/$', views.add, name='add'),
  url(r'^search/$', views.search, name='search'),
  url(r'^restaurante/(?P<id>[0-9]{8})/$', views.restaurante, name='restaurante'),
  url(r'^cities/(?P<city>[\w ]+)', views.getCity, name='cities'),
  url(r'^find/image/(?P<address>[\w ]+)', views.getPhoto, name='getPhoto'),
  url(r'^address/(?P<name>[\w|\W]+)', views.getAddress, name='address'),
  url(r'^gridfs/(?P<file_id>[0-9a-f]{24})/$', views.serve_file, name='gridfs'),
  url(r'^api/', include(router.urls, namespace='api')),
]
