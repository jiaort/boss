# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models

from duty.constants import Status, Gender


class Duty(models.Model):
    name = models.CharField(u"登记人", max_length=64)
    gender = models.SmallIntegerField(u"性别", choices=Gender.CHOICES, default=Gender.MALE)
    mobile = models.CharField(u"电话", max_length=64, null=True, blank=True)
    position = models.CharField(u"职位", max_length=64, null=True, blank=True)
    remark = models.CharField(u"备注", max_length=512, null=True, blank=True)
    registered_at = models.DateTimeField(u"登记时间", default=datetime.now)
    status = models.SmallIntegerField(u"登记状态", choices=Status.CHOICES, default=Status.UBREGISTERED)
    created_at = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    update_at = models.DateTimeField(u"最后修改时间", auto_now=True, editable=False)
