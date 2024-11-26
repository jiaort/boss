# -*- coding: utf-8 -*-

from django.conf.urls import url
from web.applicant import views

urlpatterns = [
    url(r'list/?$', views.list_view, name="applicant_list"),
    url(r'detail/(?P<a_id>[a-zA-Z0-9]+)/?$', views.detail_view, name="applicant_detail"),

    url(r'change-status/?$', views.change_status_view, name="change_applicant_status"),
    url(r'change-read/?$', views.change_read_view, name="change_applicant_read"),
    url(r'unread-count/?$', views.unread_count_view, name="unread_count"),
    url(r'export/(?P<applicant_id>[a-zA-Z0-9]+)/?$', views.export_view, name="export"),
]
