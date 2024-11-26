# -*- coding: utf-8 -*-


from datetime import datetime

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from app.account.constants import GenderType


class Account(AbstractBaseUser):
    nickname = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    gender = models.SmallIntegerField(default=GenderType.Unknown)
    app_id = models.CharField("第三方appID", null=True, max_length=20)
    auth_id = models.CharField("第三方用户id", max_length=100, default="")
    auth_token = models.CharField("token", max_length=160, default="", help_text="")
    refresh_token = models.CharField("token", max_length=160, default="", help_text="有这个token的平台是：")
    date_joined = models.DateTimeField(default=datetime.now)
    last_update = models.DateTimeField(auto_now=True)
    avatar = models.CharField(max_length=256, null=True, blank=True)
    USERNAME_FIELD = 'id'
