#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from web.manager import views


urlpatterns = [
    url(r'', include('web.manager.urls')),
]
