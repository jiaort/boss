# -* coding:utf-8 -*-

from functools import wraps
from datetime import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.urls import reverse

from utils.response import http_response
from utils.errorcode import ERRORCODE
from utils.logger.syslogger import SysLogger

from app.manager.constants import MANAGER_INFO_COOKIE_KEY
from app.manager.models import Manager


def paginate(query_set, items_per_page, page):
    paginator = Paginator(query_set, items_per_page)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return items


def get_current_user(request):
    user_info = request.session.get(USER_INFO_COOKIE_KEY)
    return user_info


def get_current_manager(request):
    manager_info = request.manager_info
    return manager_info


def render_admin(request, template, data=None):
    if not data:
        data = {}
    user_info = get_current_manager(request) or {}
    data.update({
        'user_name': user_info.get('user_name'),
        # 'user_permissions': user_info.get('permissions'),
        'manager_id': user_info.get('manager_id'),
    })
    data.update(all_perms=['ALL'])
    response = render(request, template, data)
    return response


def query_records(records, params, query_list):
    query = Q()
    for k in query_list:
        v = params.get(k)
        if not v:
            continue
        if k == 'created_time__lte':
            v = '%s 23:59:59' % v
        query &= Q(**{k: v})
    return records.filter(query)


# 装饰器验证登录
def login_check():
    def decorator(view_func):
        @wraps(view_func)
        def check_request(request, *args, **kwargs):
            try:
                session_key = request.COOKIES.get('session_id')
                manager = Manager.objects.filter(session_key=session_key, expire_time__gte=datetime.now()).first()
                if manager:
                    manager_info = {'manager_id': manager.id, 'user_name': manager.name_cn}
                    setattr(request, MANAGER_INFO_COOKIE_KEY, manager_info)
                    return view_func(request, *args, **kwargs)
            except Exception as ex:
                SysLogger.exception(ex, request)

            return HttpResponseRedirect(reverse('sso_login'))

        return check_request

    return decorator


# 装饰器验证登录
def login_check_ajax():
    def decorator(view_func):
        @wraps(view_func)
        def check_request(request, *args, **kwargs):
            status_code = ERRORCODE.UNKNOWN
            try:
                session_key = request.COOKIES.get('session_id')
                manager = Manager.objects.filter(session_key=session_key, expire_time__gte=datetime.now()).first()
                if not manager:
                    status_code = ERRORCODE.NOT_LOGIN
                else:
                    status_code = ERRORCODE.SUCCESS
                    manager_info = {'manager_id': manager.id, 'user_name': manager.name_cn}
                    setattr(request, MANAGER_INFO_COOKIE_KEY, manager_info)
                    return view_func(request, *args, **kwargs)
            except Exception as ex:
                SysLogger.exception(ex, request)

            return http_response(request, status_code=status_code)

        return check_request

    return decorator
