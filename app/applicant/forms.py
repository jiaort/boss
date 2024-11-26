#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

from app.job.constants import *
from app.applicant.constants import *


class ApplicantForm(forms.Form):
    """申请职位"""
    job_id = forms.IntegerField(label=u"工作id")
    name = forms.CharField(label=u'姓名', max_length=64)
    mobile = forms.CharField(label=u'电话', max_length=16)
    email = forms.CharField(label=u'邮箱', max_length=128)
    source = forms.ChoiceField(label=u"来源", choices=Source.CHOICES, required=False)
    education = forms.ChoiceField(label=u'最高学历', choices=Education.CHOICES)
    school = forms.CharField(label=u'毕业院校', max_length=200)
    profession = forms.CharField(label=u'所学专业', max_length=200)
    company = forms.CharField(label=u'当前公司', max_length=200)
    position = forms.CharField(label=u'当前职位', max_length=200)
    experience = forms.CharField(label=u'工作年限', max_length=50)
    file_applicant = forms.CharField(label=u'申请附件', max_length=2000, required=False)
