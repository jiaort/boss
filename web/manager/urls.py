#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from web.manager import views

urlpatterns = [
    url(r'about$', views.about_view, name='about'),
    url(r'^$', views.overview_view, name='overview'),

    url(r'^login/?$', views.login_view, name='sso_login'),
    url(r'^logout/?$', views.logout_view, name='sso_logout'),
]
