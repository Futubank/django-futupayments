# -*- coding: utf-8 -*-
from __future__ import absolute_import
try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^callback/?$', views.callback, name='futupayments_callback'),
    url('^success/$', views.success),
    url('^fail/$', views.fail),
)
