# -*- coding: utf-8 -*-
try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url
import views


urlpatterns = patterns(
    '',
    url('^$', views.callback, name='futupayments_callback'),
    url('^success/$', views.success),
    url('^fail/$', views.fail),
)
