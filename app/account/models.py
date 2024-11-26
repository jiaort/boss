# -*- coding: utf-8 -*-


from datetime import datetime

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from app.account.constants import GenderType
from app.job.constants import Education
from app.job.models import Job


class Account(AbstractBaseUser):
    nickname = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    gender = models.SmallIntegerField(default=GenderType.Unknown)
    app_id = models.CharField(u"第三方appID", null=True, max_length=20)
    auth_id = models.CharField(u"第三方用户id", max_length=100, default="")
    auth_token = models.CharField(u"token", max_length=160, default="", help_text="")
    refresh_token = models.CharField(u"token", max_length=160, default="", help_text="有这个token的平台是：")
    date_joined = models.DateTimeField(default=datetime.now)
    last_update = models.DateTimeField(auto_now=True)
    avatar = models.CharField(max_length=256, null=True, blank=True)
    USERNAME_FIELD = 'id'


class Resume(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, db_constraint=False, unique=True)
    name = models.CharField(u"姓名", max_length=64, null=True)
    mobile = models.CharField(u"电话", max_length=16, null=True)
    email = models.CharField(u"邮箱", max_length=128, null=True)
    education = models.SmallIntegerField(u"最高学历", choices=Education.CHOICES, default=Education.Other)
    school = models.CharField(u"毕业院校", max_length=200, null=True)
    profession = models.CharField(u"所学专业", max_length=200, null=True)
    company = models.CharField(u"当前公司", max_length=200, null=True)
    position = models.CharField(u"当前职位", max_length=200, null=True)
    experience = models.CharField(u"工作年限", max_length=50, null=True)
    file = models.CharField(u"简历附件", max_length=200, blank=True, null=True)
    file_applicant = models.CharField(u"申请附件", max_length=2000, blank=True, null=True)


class Favorite(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, db_constraint=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        index_together = [['account_id'], ['job_id']]
