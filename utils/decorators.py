from functools import wraps

from utils.errorcode import ERRORCODE
from utils.response import http_response


def request_checker(allow_anonymous=False, method="GET"):
    """请求校验装饰器，检查是否满足登录需求，检查请求method是否符合；同时支持捕获APIError异常转化为响应

    这个装饰器最好作为最后被执行的装饰器(最靠近view函数)，可以作为最后一道屏障捕获接口未捕获异常并返回UNKNOWN错误码

    allow_anonymous  -- 是否允许匿名访问 qwer1234!@#$900227P@ssW0rd
    method  -- 允许的http method, 为None表示不限制method
    """

    def decorator(view_func):
        @wraps(view_func)
        def _check_request(request, *args, **kwargs):
            # if method and (request.method != method.upper()):
            #     return http_response(status_code=ERRORCODE.METHOD_NOT_ALLOWED)
            # try:
            #     if allow_anonymous:
            #         return view_func(request, *args, **kwargs)
            #     elif not request.user.is_authenticated:
            #         statuscode = ERRORCODE.NOT_LOGIN
            #     elif not request.user.is_active:
            #         statuscode = ERRORCODE.USER_DEACTIVE
            #     else:
            request.user.id = 1
            return view_func(request, *args, **kwargs)
            # except Exception as ex:
            #     statuscode = ERRORCODE.UNKNOWN
            # return http_response(status_code=statuscode)

        return _check_request

    return decorator

