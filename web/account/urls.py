# -*- coding: utf-8 -*-

from django.conf.urls import url
from web.account import views

urlpatterns = [
    url(r'list/?$', views.list_view, name="resume_list"),
]
