#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError

from app.account.models import Account


class AddUserForm(forms.ModelForm):

    class Meta:
        model = Account
        exclude = ('password', 'last_login', 'is_active', 'session_key', 'company_id')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=u'旧密码', required=True, max_length=128, widget=forms.PasswordInput())
    new_password = forms.CharField(label=u'新密码', required=True, max_length=128, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label=u'确认新密码', required=True, max_length=128, widget=forms.PasswordInput())

    def clean_confirm_password(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            raise ValidationError(message='请确认两次输入的新密码一致')
        return self.cleaned_data['confirm_password']


class UserForm(forms.Form):
    name_cn = forms.CharField(max_length=20, required=False)
    name_sn = forms.CharField(max_length=20, required=False)
    bid = forms.CharField(max_length=30, required=False)
    invite_code = forms.CharField(max_length=10, required=False)
    self_code = forms.CharField(max_length=10, required=False)
    start_time = forms.CharField(required=False)
    end_time = forms.CharField(required=False)
    audit_status = forms.IntegerField(required=False)
    position = forms.IntegerField(required=False)
