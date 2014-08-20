# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.conf import settings
try:
    from django.conf.urls.defaults import patterns, url, include
except ImportError:
    from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^futupayments/', include('futupayments.urls')),
)

if 'app' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', url(r'^$', 'app.views.home', name='home'))
