# -*- coding: utf-8 -*-

from django.conf.urls import url
from web.document import views

urlpatterns = [
    url(r'incoming_list/?$', views.incoming_list_view, name="incoming_list"),
    url(r'outgoing_list/?$', views.outgoing_list_view, name="outgoing_list"),
]
