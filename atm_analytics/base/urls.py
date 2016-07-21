from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^i18n/', views.set_language, name='set_lang'),
    url(r'^$', views.dashboard, name='dashboard'),
]
