# -*- coding: utf-8 -*-

from urllib import parse
from django.utils.encoding import smart_str
from datetime import datetime
from django.conf import settings


def form_error(form_info):
    error_str = []
    for k, v in form_info.errors.items():
        if k == "__all__":
            error_str.append(v[0])
        else:
            error_str.append("%s:%s" % (form_info.fields[k].label, v[0]))
    return error_str


def get_host(request):
    host = request.get_host().split(':')[0].lower()
    domain = settings.SESSION_COOKIE_DOMAIN
    for item in settings.SESSION_HOST_DOMAIN:
        if host.endswith(item.lower()):
            domain = item
            break
    return domain


def gen_prefix(salt):
    if salt:
        return str(salt) + '_' + datetime.now().strftime("%y%m%d%H%M%S") + '_'
    else:
        return datetime.now().strftime("%y%m%d%H%M%S") + '_'


def upload_file(file_obj, salt=None):
    """
    上传文件
    """
    if not file_obj:
        return '', ''
    try:
        prefix = gen_prefix(salt)
        file_path = prefix + parse.quote(file_obj.name.encode('utf8'))  # 支持中文
        save_path = 'media/' + prefix + smart_str(file_obj.name)
        destination = open(save_path, 'wb+')
        for chunk in file_obj.chunks():
            destination.write(chunk)
        destination.close()
        return True, file_path
    except Exception as exp:
        return exp, ''


def get_choice_id(choices, name):
    for item in choices:
        if item[1] == name:
            return item[0]
    return None
