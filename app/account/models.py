# -*- coding: utf-8 -*-


from datetime import datetime

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class Account(AbstractBaseUser):
    auth_id = models.CharField("第三方用户id", max_length=100, default="")
    date_joined = models.DateTimeField(default=datetime.now)
    last_update = models.DateTimeField(auto_now=True)
    usage_count = models.IntegerField(default=3)
    expired_time = models.DateTimeField(default=datetime.now)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'id'
