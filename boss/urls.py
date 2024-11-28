# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    url(r'^api/boss/', include('app.urls')),
    url(r'^', include('web.urls')),

    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT})
]
