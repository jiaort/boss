#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import urllib

from django import template

register = template.Library()


@register.filter
def has_perms(permissions, perms):
    perms = perms.split(',')

    for permission in permissions:
        if 'ALL' in permission:
            return True
        for perm in perms:
            if perm in permission:
                return True
    return False


@register.filter
def fen_to_yuan(amount):
    if not amount:
        return 0
    return amount / 100.0


@register.filter
def suffix_available(file_path):
    if os.path.splitext(file_path)[-1] in ['.docx', '.doc']:
        return True

    return False


@register.filter
def file_name(file_path):
    return urllib.parse.unquote(file_path.split('_', 2)[-1])
