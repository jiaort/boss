# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from app.job import views


urlpatterns = [
    url(r'job-list/?$', views.job_list_view),
]
