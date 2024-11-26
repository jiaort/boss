# -*- coding: utf-8 -*-

from django.conf.urls import url

from app.account import views


urlpatterns = [
    url(r'^favorite-list/?$', views.favorite_list_view),
    url(r'^favorite/?$', views.favorite_view),
    url(r'^resume/?$', views.resume_view),
    url(r'^edit-resume/?$', views.edit_resume_view),
    url(r'^upload-resume/?$', views.upload_resume_view),
    url(r'^upload-file/?$', views.upload_file_view),

    # 认证
    url(r'^callback-weixin/?$', views.callback_weixin_view),
    url(r'^get-sign-info/?$', views.get_sign_info_view),
]
