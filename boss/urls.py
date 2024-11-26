# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.views.static import serve
from web.manager import views
from django.conf import settings


urlpatterns = [
    url(r'^api/boss/', include('app.urls')),
    url(r'^admin/', include('web.urls')),

    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT})
]
