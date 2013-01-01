from django.conf.urls import patterns, url
from django.conf import settings
from game import views
import os

urlpatterns = patterns('',
    url(r'^status$', views.status, name='status'),
    url(r'^move/(?P<id>\d+)/$', views.move, name='move'),
    url(r'^shoot/(?P<id>\d+)/$', views.shoot, name='shoot'),
    url(r'^reset$', views.reset, name='reset'),
    url(r'^media/(?P<path>.*)$', "django.views.static.serve", {'document_root': settings.MEDIA_ROOT})
)

