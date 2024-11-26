# -*- coding: utf-8 -*-

from django.db import models

from app.account.models import Account
from app.job.models import Job
from app.job.constants import Education
from app.applicant.constants import Source, Status


class Applicant(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, db_constraint=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, db_constraint=False)
    name = models.CharField(u"应聘者姓名", max_length=64)
    mobile = models.CharField(u"电话", max_length=16)
    email = models.CharField(u"邮箱", max_length=128)
    source = models.SmallIntegerField(u"来源", choices=Source.CHOICES, default=Source.All)
    education = models.SmallIntegerField(u"学历", choices=Education.CHOICES, default=Education.Other)
    school = models.CharField(u"毕业院校", max_length=200)
    profession = models.CharField(u'所学专业', max_length=200)
    company = models.CharField(u'当前公司', max_length=200)
    position = models.CharField(u"当前职位", max_length=200)
    experience = models.CharField(u'工作年限', max_length=50)
    file_applicant = models.CharField(u"申请附件", max_length=2000, blank=True, null=True)
    read = models.BooleanField(u"读取状态", default=False)
    status = models.SmallIntegerField(u"处理状态", choices=Status.CHOICES, default=Status.New)
    created_time = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    last_update = models.DateTimeField(u"最后修改时间", auto_now=True, editable=False)
