from datetime import datetime

from app.account.backends import wx_code_login
from app.account.forms import LoginForm
from app.account.models import Account
from utils.errorcode import ERRORCODE
from utils.response import http_response
from utils.jwt import JWTAuth
from utils.decorators import form_validator, api_sso_checker


@form_validator(LoginForm)
@api_sso_checker(allow_anonymous=True, method="POST")
def login_view(request):
    """
    微信回调登陆接口
    :Args request: code 微信回调code
    :return:
    """
    form = LoginForm(request.GET)
    if not form.is_valid():
        return http_response(status_code=ERRORCODE.PARAM_ERROR)

    code = form.cleaned_data.get("code")
    user = wx_code_login(code=code)
    if not user:
        return http_response(status_code=ERRORCODE.PROVIDER_PLATFORM_ERROR)
    data = {
        "user_id": user.id,
        "auth_id": user.auth_id,
        "usage_count": user.usage_count,
        "expired_time": user.expired_time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    to_encode = data.copy()
    data["token"] = JWTAuth().jwt_encode(to_encode)
    return http_response(
        context=data,
        status_code=ERRORCODE.SUCCESS
    )


@api_sso_checker()
def user_info_view(request):
    """
    用户信息接口
    :param request:
    :return:
    """
    user_id = request.user_id
    user = Account.objects.filter(id=user_id).first()
    if not user:
        return http_response(status_code=ERRORCODE.NOT_FOUND)
    return http_response(
        context={
            "user_id": user.id,
            "auth_id": user.auth_id,
            "usage_count": user.usage_count,
            "expired_time": user.expired_time.strftime('%Y-%m-%d %H:%M:%S'),
        },
        status_code=ERRORCODE.SUCCESS
    )


@api_sso_checker()
def convert_view(request):
    """
    消费次数接口
    :param request:
    :return:
    """
    user_id = request.user_id
    user = Account.objects.filter(id=user_id).first()
    if not user:
        return http_response(status_code=ERRORCODE.NOT_FOUND)
    if user.expired_time > datetime.now():
        return http_response(ERRORCODE.SUCCESS)
    if user.usage_count <= 0:
        return http_response(ERRORCODE.TIMES_NOT_ENOUGH)
    user.usage_count -= 1
    user.save()
    return http_response(status_code=ERRORCODE.SUCCESS)
