# -*- coding: utf-8 -*-

from django.conf.urls import url

from app.account import views


urlpatterns = [
    url(r'^login/?$', views.login_view),
    url(r'^user_info/?$', views.user_info_view),
    url(r'^convert/?$', views.convert_view),
]
