from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^config/$', views.config, name='config'),
    url(r'^create-xfs-format/$', views.create_xfs_format, name='create_xfs_format'),
    url(r'^delete-xfs-format/(?P<xfs_format_id>\d+)/$', views.delete_xfs_format, name='delete_xfs_format'),
    url(r'^xfs-format/(?P<xfs_format_id>\d+)/$', views.update_xfs_format, name='update_xfs_format'),
]
