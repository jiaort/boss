#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from web.account import views

urlpatterns = [
    url(r'account_list$', views.account_list_view, name='account_list'),
]
