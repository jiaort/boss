from datetime import datetime
from django.conf import settings
from django.db.models import Count
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import logout

from utils.response import http_response
from utils.errorcode import ERRORCODE

from app.manager.constants import MANAGER_INFO_COOKIE_KEY
from app.manager.models import Manager

from web.decorators import render_admin, login_check
from web.manager.backend import do_login


@login_check()
def overview_view(request):
    data = {
        'active_classes': ['.home-menu'],
        'job_count': 1,
        'applicant_count': 2,
        'today_applicant_count': 2,
        'resume_count': 2,
        'status_titles': "dddd",
        'status_counts': 2,
        'campus_counts': 2,
        'social_counts': 21,
    }
    return render_admin(request, 'manager/home.html', data)


def login_view(request):
    """
    用户登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'manager/login.html', {'back_url': ''})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        manager = Manager.objects.filter(name_cn=username).first()
        if manager:
            if manager.check_password(password):
                response = http_response(status_code=ERRORCODE.SUCCESS)
                do_login(response, manager)

                return response
            else:
                return http_response(status_code=ERRORCODE.FAILED, msg_cn='密码错误')
        else:
            return http_response(status_code=ERRORCODE.FAILED, msg_cn='用户名错误')


def logout_view(request):
    """
    用户登出
    :param request:
    :return:
    """
    logout(request)
    back_url = request.GET.get('back_url') or ''
    response = HttpResponseRedirect(reverse('sso_login') + (('?back_url=%s' % back_url) if back_url else ''))
    response.delete_cookie(
        MANAGER_INFO_COOKIE_KEY,
        domain=settings.SESSION_COOKIE_DOMAIN,
    )
    return response


def about_view(request):
    return render_admin(request, 'manager/about.html')


def user_detail(request, user_id):
    """
    查看用户信息
    """
    return render_admin(request, 'manager/account_detail.html')


def user_detail_view(request, user_id):
    """
    管理员查看用户的信息
    """
    return user_detail(request, user_id)


def self_detail_view(request):
    """
    查看自己的信息
    """
    return user_detail(request, request.user.id)


def add_account_view(request):
    data = {
        'active_classes': ['.account', '.account-list'],
    }
    return render_admin(request, 'manager/add_account.html', data)


def change_password_view(request):
    data = {}
    return render_admin(request, 'manager/change_password.html', data)


def list_account_view(request):
    """普通注册用户列表"""
    data = {}
    return render_admin(request, 'manager/list_account.html', data)


def ban_user_view(request, user_id):
    return HttpResponseRedirect(reverse('user_detail', args=(user_id,)))


def reset_user_passwd_view(request, user_id):
    return HttpResponseRedirect(reverse('user_detail', args=(user_id,)))


def edit_user_name_view(request):
    return HttpResponseRedirect(reverse('user_detail', args=''))


def register_view(request):
    """
    员工注册
    :param request:
    :return:
    """
    tp = 'sso/register.html'
    back_url = request.parameters.get('back_url')

    return render(request, tp, {'back_url': back_url})


def staff_list_view(request):
    """员工列表"""
    data = {}
    return render_admin(request, 'manager/staff_list.html', data)
