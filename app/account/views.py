import hashlib
import time
from uuid import uuid4

from django.db.models import Q
from django.http import HttpResponseRedirect
from app.account.auth.client import WeixinAuth
from app.account.backends import wx_code_login
from app.account.forms import WechatWebAuthForm, AuthorizerAppIdForm
from config.oauth_client import OauthConfig
from utils.decorators import request_checker
from utils.errorcode import ERRORCODE
from utils.response import http_response


@request_checker(allow_anonymous=True)
def callback_weixin_view(request):
    """
    微信回调接口
    :param request:
    :return:
    """
    form = WechatWebAuthForm(request.GET)
    if not form.is_valid():
        # 参数不对, todo 跳转到其他页面
        return http_response(status_code=ERRORCODE.PARAM_ERROR)

    code = form.cleaned_data.get("code")
    next_url = form.cleaned_data.get("next")

    user, _ = wx_code_login(request=request, code=code)
    if user:
        response = HttpResponseRedirect(next_url)
        return response
    else:
        return HttpResponseRedirect(next_url)


@request_checker(allow_anonymous=True)
def get_sign_info_view(request):
    """
    获取ticket接口
    :param request:
    :return:
    """
    form = AuthorizerAppIdForm(request.GET)
    if not form.is_valid():
        return http_response(status_code=ERRORCODE.PARAM_ERROR)

    url = form.cleaned_data.get("url")
    appkey = OauthConfig.get(OauthConfig.WeiXinWeb)["key"]
    wx_auth_client = WeixinAuth(appkey)
    jsapi_ticket = wx_auth_client.get_ticket()
    sign_fields = {
        "appid": appkey,
        "jsapi_ticket": jsapi_ticket,
        "noncestr": uuid4().hex,
        "timestamp": int(time.time()),
        "url": url,
    }
    sign_str = "jsapi_ticket={jsapi_ticket}&noncestr={noncestr}&timestamp={timestamp}&url={url}".format(**sign_fields)
    sign_fields.pop("jsapi_ticket")
    sign_fields["sign"] = hashlib.sha1(sign_str.encode("utf8")).hexdigest()

    return http_response(context=sign_fields, status_code=ERRORCODE.SUCCESS)
