# -*- coding: utf-8 -*-

from django import forms


class WechatWebAuthForm(forms.Form):
    code = forms.CharField(max_length=32, required=False)
    state = forms.CharField(max_length=128, required=False)
    next = forms.CharField(max_length=2000, required=False)
    app_id = forms.CharField(max_length=20, required=False)


class AuthorizerAppIdForm(forms.Form):
    url = forms.CharField(max_length=1024)
