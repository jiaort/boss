# -*- coding: utf-8 -*-
from datetime import date

from django.db import models

from document.constants import SecretHierarchy


class IncomingDocument(models.Model):
    title = models.CharField(u"文件名", max_length=64, null=True, blank=True)
    number = models.CharField(u"文号", max_length=64, null=True, blank=True)
    secret = models.SmallIntegerField(u"密级", choices=SecretHierarchy.CHOICES, default=SecretHierarchy.TOP_SECRET)
    units = models.CharField(u"发件单位", max_length=64, null=True, blank=True)
    senders = models.CharField(u"发件人", max_length=64, null=True, blank=True)
    sender_at = models.DateField(u"发件日期", null=True, blank=True)
    recipient_at = models.DateField(u"签收日期", null=True, blank=True)
    expires = models.IntegerField(u"保密期限", null=True, blank=True)
    registrant = models.CharField(u"登记人", null=True, blank=True)
    content = models.TextField(u"文章内容")
    created_at = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    update_at = models.DateTimeField(u"最后修改时间", auto_now=True, editable=False)


class OutgoingDocument(models.Model):
    title = models.CharField(u"文件名", max_length=64, null=True, blank=True)
    number = models.CharField(u"文号", max_length=64, null=True, blank=True)
    secret = models.SmallIntegerField(u"密级", choices=SecretHierarchy.CHOICES, default=SecretHierarchy.TOP_SECRET)
    units = models.CharField(u"接收单位", max_length=64, null=True, blank=True)
    recipients = models.CharField(u"发件人", max_length=64, null=True, blank=True)
    contact = models.CharField(u"联系方式", max_length=64, null=True, blank=True)
    registered_at = models.DateField(u"发件日期", null=True, blank=True)
    expires = models.IntegerField(u"保密期限", null=True, blank=True)
    registrant = models.CharField(u"登记人", null=True, blank=True)
    created_at = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    content = models.TextField(u"文章内容")
    update_at = models.DateTimeField(u"最后修改时间", auto_now=True, editable=False)
