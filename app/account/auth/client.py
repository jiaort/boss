# -*- coding: utf-8  -*-
import json
from datetime import datetime

from config.oauth_client import OauthConfig
from utils.errorcode import ERRORCODE
from utils.request_client import RequestClient


class Oauth20API(object):
    """
    基于Oauth2.0基础协议 code token 获得用户信息
    """

    def __init__(self, code=None, token=None):
        self.code = code
        self.token = token
        self.request_conf = None
        self.user_id = None
        self.user_info = {}  # {"nickname": "", "gender": 0, "description": "", "avatar": ""}
        self.error = ERRORCODE.PROVIDER_PLATFORM_ERROR

    @classmethod
    def _get_headers(cls, add_sep_headers, headers):
        default_headers = {}
        if add_sep_headers:  # 默认的头部
            default_headers = {
                "Accept-Language": "zh_CN",
                "User-Agent": "sep",
                "Connection": "Keep-Alive",
            }
        if headers and isinstance(headers, dict):
            default_headers.update(headers)

        return default_headers

    def gen_request_token_param(self):
        """
        生成获取token参数
        """
        params = {
            "client_id": self.request_conf.get("key"),
            "client_secret": self.request_conf.get("secret"),
            "grant_type": "authorization_code",
            "code": self.code,
            "redirect_uri": self.request_conf.get("default"),
        }
        self.request_token_param = params

    def request_token(self, method="GET", output="json"):
        """
        获取token请求
        :param method:请求方式POST/GET
        :return:请求返回的内容data
        """
        response = RequestClient.query(url=self.request_conf.get("token"), method=method, params=self.request_token_param)
        if response and response.status_code == 200:
            return response.json() if output == "json" else response
        return None

    def get_token(self):
        """
        解析请求返回数据，获得token值
        :return:token值
        """
        return None

    def gen_request_id_param(self):
        """
        生成获取用户id参数
        """
        params = {
            "source": self.request_conf.get("key"),
            "access_token": self.token,
        }
        self.request_id_param = params

    def request_id(self, method="GET", output="json"):
        """
        获取id请求
        :param method:请求方式POST/GET
        :return:请求返回的内容data
        """
        response = RequestClient.query(
            url=self.request_conf.get("get_id"), method=method, params=self.request_id_param
        )
        if response and response.status_code == 200:
            return response.json() if output == "json" else response
        return None

    def get_id(self):
        """
        解析请求返回数据，获得id值
        :return:id值
        """
        return ""

    def gen_request_user_info_param(self):
        """
        生成获取用户信息参数
        """
        self.request_user_info_param = None

    def request_user_info(self, method="GET", output="json", encoding=None):
        """
        获取用户信息请求
        :param method:请求方式POST/GET
        :return:请求返回的内容data
        """
        response = RequestClient.query(
            url=self.request_conf.get("get_user_info"), method=method,
            params=self.request_user_info_param)
        if response and response.status_code == 200:
            if encoding:
                response.encoding = encoding
            return response.json() if output == "json" else response
        return None

    def get_user_info(self):
        """
        解析请求返回数据，获得用户信息
        :return:用户信息
        """
        return {}


class WeiXinOauth(Oauth20API):
    def __init__(self, code=None, token=None, openid=None, wx_config=None):
        Oauth20API.__init__(self, code, token)
        self.user_id = openid

        if wx_config:
            self.request_conf = wx_config
        else:
            self.request_conf = OauthConfig.get(OauthConfig.WeiXinWeb)

    def gen_request_token_param(self):
        """
        生成获取token参数
        """
        params = {
            "appid": self.request_conf.get("key"),
            "secret": self.request_conf.get("secret"),
            "grant_type": "authorization_code",
            "code": self.code,
        }
        self.request_token_param = params

    def get_token(self):
        self.gen_request_token_param()
        data = self.request_token(method="GET", output="json")
        if data and "access_token" in data:
            self.token = data.get('access_token', None)
            self.expires_in = data.get('expires_in', None)  # 该access token的有效期，单位为秒。
            self.user_id = data.get("openid")
        elif data and hasattr(data, 'errcode') and hasattr(data, 'errmsg'):
            self.error["code"] = data.get('errcode', self.error["code"])
            self.error["msg"] = data.get("errmsg", self.error["msg"])

        return self.token

    def get_openid(self):
        self.gen_request_token_param()
        data = self.request_token(method="GET", output="json")
        if data and "openid" in data:
            self.expires_in = data.get('expires_in', None)  # 该access token的有效期，单位为秒。
            self.user_id = data.get("openid")
        elif data and hasattr(data, 'errcode') and hasattr(data, 'errmsg'):
            self.error["code"] = data.get('errcode', self.error["code"])
            self.error["msg"] = data.get("errmsg", self.error["msg"])

        return self.user_id

    def gen_request_user_info_param(self):
        params = {
            "access_token": self.token,
            "openid": self.user_id,
        }

        self.request_user_info_param = params

    def get_user_info(self, third_app_id='', component_access_token=''):
        """
        api 文档:  https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&lang=zh_CN
        """
        # 方便code验证
        if not (self.token or self.code):
            return {}
        if not self.token:
            self.get_token()

        if not (self.user_id and self.token):
            return {}

        self.gen_request_user_info_param()
        response = self.request_user_info(encoding="utf-8")
        if response and "openid" in response:
            self.user_info["nickname"] = response.get('nickname', None)
            self.user_info["avatar"] = response.get('headimgurl', None)
            # 针对一个微信开放平台帐号下的应用，同一用户的unionid是唯一的;openid普通用户的标识，对当前开发者帐号唯一
            self.unionid = response.get("unionid", None)
            self.user_info["gender"] = response.get('sex', 0)
        elif response and "errcode" in response:
            self.error["code"] = response.get('errcode', self.error["code"])
            self.error["msg"] = response.get("errmsg", self.error["msg"])

        return self.user_info


class WeixinAuth(object):
    """
    微信认证,获取access_token与ticket
    """
    cache_key_format = "TOKEN:{appkey}"
    accessToken_url = "https://api.weixin.qq.com/cgi-bin/token"
    ticket_url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket"
    TS_LIMIT = 7200 - 60 * 10   # 有效期前10分钟开始替换

    def __init__(self, appkey):
        self.appkey = appkey
        self.cache_key = self.cache_key_format.format(appkey=appkey)

    def get_conf(self):
        return OauthConfig.get(OauthConfig.WeiXinWeb)

    def _get_access_token_from_wx(self):
        """
        从微信获取access_token
        限制频率 0/2000
        {
            "access_token": "lekWHjhNZ1G0MQoFGEZKrYbZEr3pIq2XRl..."
            "expires_in": 7200
        }
        :return:
        """
        conf = self.get_conf()
        if not conf:
            return None
        response = RequestClient.query(self.accessToken_url, params={
            "grant_type": "client_credential",
            "appid": conf["key"],
            "secret": conf["secret"],
        })
        if response.status_code == 200:
            return response.json()["access_token"]

    def _get_ticket_from_wx(self, access_token):
        """
        从微信获取ticket
        限制频率 0/100000
        {
            "errcode": 0
            "errmsg": "ok"
            "ticket": "bxLdikRXVbTPdHSM05e5u7-QOpRDBCPEZRZ_gqzK..."
            "expires_in": 7200
        }
        :return:
        """
        response = RequestClient.query(self.ticket_url, params={
            "access_token": access_token,
            "type": "jsapi",
        })
        if response.status_code == 200:
            return response.json()["ticket"]

    def _sync_and_set_cache_ticket(self):
        """
        同步并更新缓存中的ticket

        :return: ticket or None
        """
        access_token = self._get_access_token_from_wx()
        ticket = self._get_ticket_from_wx(access_token)
        if ticket:
            with open("ticket.txt", 'w') as ticket_file:
                file = {
                    "ticket": ticket,
                    "expire": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                ticket_file.write(json.dumps(file))

            return ticket

    def get_ticket(self):
        """
        获取ticket，先从缓存（redis）获取，过期了就同步新的ticket
        :return:
        """
        with open("ticket.txt", 'r') as ticket_file:
            file = ticket_file.read()
            if file:
                ticket_dict = json.loads(file)
                pass_time = (datetime.now() - datetime.strptime(ticket_dict["expire"], '%Y-%m-%d %H:%M:%S')).seconds
                if pass_time > self.TS_LIMIT:
                    return self._sync_and_set_cache_ticket()
                else:
                    return ticket_dict["ticket"]
            else:
                return self._sync_and_set_cache_ticket()
