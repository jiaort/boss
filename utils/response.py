# -*- coding: utf-8 -*-

import time
import json

from django.conf import settings
from django.http import HttpResponse


def http_response(context={}, status_code=None, code=None, msg=None, msg_cn=None, content_type=None):
    """
    统一的http response封装，增加通用返回参数，返回值为HttpResponse对象

    默认情况下，output为json时返回content-type为application/json, jsonp时返回content-type为application/javascript,
    可以通用content_type改变content-type的默认行为

    :param request: django请求对象
    :param context: 响应数据字典 type:dict
    :param status_code: 错误状态对象
    :param code: 自定义错误码，为空则使用`status_code`的错误码
    :param msg: 自定义错误信息，为空则使用`status_code`的msg
    :param msg_cn: 自定义中文错误信息，为空则使用`status_code`的msgcn
    :param content_type:

    :return str 序列化json数据或pb流
    """
    content_dict = {
        'version': settings.VERSION,
        'code': code if code is not None else status_code.code if status_code else '',
        'msg': msg if msg is not None else status_code.msg if status_code else '',
        'msg_cn': msg_cn if msg_cn is not None else status_code.msgcn if status_code else '',
        'timestamp': int(time.time()),
    }
    content_dict.update(context)
    print(content_dict)
    response_content = json.dumps(content_dict)

    content_type = content_type or 'application/json'
    return HttpResponse(response_content, content_type=content_type)
