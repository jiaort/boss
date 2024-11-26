#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include


urlpatterns = [
    url(r'account/', include('app.account.urls')),
    url(r'job/', include('app.job.urls')),
    url(r'applicant/', include('app.applicant.urls')),
]
