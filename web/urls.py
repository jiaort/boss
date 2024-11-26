#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from web.manager import views


urlpatterns = [
    url(r'manager/', include('web.manager.urls')),

    url(r'about$', views.about_view, name='about'),
    url(r'^$', views.overview_view, name='overview'),

    url(r'^login/?$', views.login_view, name='sso_login'),
    url(r'^logout/?$', views.logout_view, name='sso_logout'),
]
