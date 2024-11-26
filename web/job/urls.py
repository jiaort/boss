#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from web.job import views

urlpatterns = [
    url(r'list/?$', views.list_view, name="job_list"),
    url(r'job/?$', views.job_view, name="job_new_view"),
    url(r'job/(?P<job_id>[a-zA-Z0-9]+)/?$', views.job_view, name="job_view"),
    url(r'edit/?$', views.edit_view, name="edit_new_job"),
    url(r'edit/(?P<job_id>[a-zA-Z0-9]+)/?$', views.edit_view, name="edit_job"),
]
