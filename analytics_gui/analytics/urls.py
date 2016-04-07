from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create$', views.create, name='create'),
    url(r'^case/(?P<case_id>\d+)/$', views.view_case, name='view_case'),
    url(r'^delete/(?P<case_id>\d+)/$', views.delete_case, name='delete_case'),
    url(r'^analyze/(?P<case_id>\d+)/$', views.analyze_case, name='analyze'),
    url(r'^analyze/(?P<case_id>\d+)/generate_pdf/$', views.generate_pdf, name='generate-pdf'),
    url(r'^no-format-available-2-analyze/$', views.no_format_available, name='no-format-available-2-analyze'),
]
