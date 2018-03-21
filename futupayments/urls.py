from django.conf.urls import url

from . import views


urlpatterns = [
    url('^callback/?$', views.callback, name='futupayments_callback'),
    url('^success/?$', views.success),
    url('^fail/?$', views.fail),
]
