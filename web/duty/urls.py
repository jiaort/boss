# -*- coding: utf-8 -*-

from django.conf.urls import url
from web.duty import views

urlpatterns = [
    url(r'list/?$', views.list_duty_view, name="duty_list"),
    url(r'get/(?P<duty_id>[a-zA-Z0-9]+)/?$', views.get_duty_view, name="duty_get"),
    url(r'create/?$', views.create_duty_view, name="duty_create"),
    url(r'edit/(?P<duty_id>[a-zA-Z0-9]+)/?$', views.create_duty_view, name="duty_edit"),
]
