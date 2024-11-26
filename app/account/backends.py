import string
from random import choice

from django.contrib.auth import login
from app.account.constants import GenderType
from app.account.models import Account
from app.account.auth.client import WeiXinOauth
from config.oauth_client import OauthConfig
from utils.errorcode import ERRORCODE


def gen_secret_key(length=40):
    KEY_CHARACTERS = string.ascii_letters + string.digits
    return ''.join([choice(KEY_CHARACTERS) for _ in range(length)])


def easy_gen_nickname(nickname=""):
    if not nickname:
        nickname = gen_secret_key(6)

    return nickname


def wx_code_login(request, code=""):
    """第三方登录

    code -- 微信授权code
    return -- User, STATUS_CODE"""
    oauth_client = WeiXinOauth(code=code)
    oauth_client.get_openid()
    user_info = {"openid": oauth_client.user_id}

    if user_info and oauth_client.user_id:

        nickname = easy_gen_nickname(nickname=user_info.get("nickname", ""))
        user = Account.objects.filter(auth_id=oauth_client.user_id).first()

        if not user:
            user = Account.objects.create(
                nickname=nickname,
                gender=user_info.get("gender") or GenderType.Unknown,
                avatar=user_info.get("avatar") or "",
                auth_id=oauth_client.user_id,
                app_id=OauthConfig.get(OauthConfig.WeiXinWeb)['key'],
                auth_token=oauth_client.token or "",
            )

        login(request, user)
        return user, ERRORCODE.SUCCESS
    else:
        # 返回错误
        return None, oauth_client.error or ERRORCODE.PROVIDER_PLATFORM_ERROR
