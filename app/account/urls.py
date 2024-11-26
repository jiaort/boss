# -*- coding: utf-8 -*-

from django.conf.urls import url

from app.account import views


urlpatterns = [
    # 认证
    url(r'^callback-weixin/?$', views.callback_weixin_view),
    url(r'^get-sign-info/?$', views.get_sign_info_view),
]
