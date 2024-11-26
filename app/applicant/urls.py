# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from app.applicant import views


urlpatterns = [
    url(r'applicant-list/?$', views.applicant_list_view),
    url(r'applicant/?$', views.applicant_view),
]
