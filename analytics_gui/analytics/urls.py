from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^create$', views.create, name='create'),
    url(r'^case/(?P<case_id>\d+)/$', views.view_case, name='view_case'),
]