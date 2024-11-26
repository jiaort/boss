# -*- coding: utf-8 -*-

from django import forms


class ApplicantListForm(forms.Form):
    name = forms.CharField(label=u'姓名', max_length=64, required=False)
    job_title = forms.CharField(label=u'职位名称', max_length=200, required=False)
    status = forms.IntegerField(label=u"处理状态", required=False)
    status_order = forms.IntegerField(label=u"处理状态排序", required=False)
    read = forms.IntegerField(label=u"阅读状态", required=False)
    read_order = forms.IntegerField(label=u"阅读状态排序", required=False)

