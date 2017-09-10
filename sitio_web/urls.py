"""sitio_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin

# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
		return '/'

urlpatterns = [
	url(r'^', include('restaurantes.urls')),
    url(r'^admin/', admin.site.urls),
	url(r'^accounts/', include('registration.backends.simple.urls')),
	url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^tokenauth/obtain-auth-token/$', csrf_exempt(obtain_auth_token)),
]
