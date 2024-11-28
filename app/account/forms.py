# -*- coding: utf-8 -*-

from django import forms


class LoginForm(forms.Form):
    code = forms.CharField(max_length=32)
    next_url = forms.CharField(max_length=2000, required=False)
