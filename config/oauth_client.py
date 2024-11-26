# -*- coding: utf-8 -*-


class OauthConfig(object):
    WeiXinWeb = 4

    DICT = [
        {
            "id": WeiXinWeb,
            "key": "wx96ec9d191e5fed95",
            "secret": "377ea2069d3a6eaf6fbcae6d71d6891b",
            "callback": "",
            "authorize": "",
            "third_token": "https://api.weixin.qq.com/sns/oauth2/component/access_token",
            "token": "https://api.weixin.qq.com/sns/oauth2/access_token",
            "easy_token": "https://api.weixin.qq.com/cgi-bin/token",
            "get_id": "",
            "get_user_info": "https://api.weixin.qq.com/sns/userinfo",
            "easy_get_user_info": "https://api.weixin.qq.com/cgi-bin/user/info",
            "redirect": "",
            "default": "",
        }
    ]

    @classmethod
    def get(cls, value, key="id"):
        """暂时使用"""
        for d in cls.DICT:
            if d[key] == value:
                return d
        return {}
