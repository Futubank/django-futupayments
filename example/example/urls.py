from django.conf import settings
from django.conf.urls import url
from django.urls import include


urlpatterns = [
    url(r'^futupayments/', include('futupayments.urls')),
]


if 'app' in settings.INSTALLED_APPS:
    from app import views
    urlpatterns += [
        url(r'^$', views.home, name='home'),
    ]
