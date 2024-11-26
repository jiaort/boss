# -*- coding: utf-8 -*-

from django import forms


class ResumeForm(forms.Form):
    """查询简历"""
    name = forms.CharField(label=u'姓名', max_length=64, required=False)
