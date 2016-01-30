from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^config/$', views.config, name='config'),
]
