import traceback
from functools import wraps

from loguru import logger

from utils.errorcode import ERRORCODE
from utils.response import http_response
from utils.jwt import JWTAuth


def form_validator(form_class):
    """
    表单验证装饰器，用于在执行视图函数之前验证 Django 表单。

    Args:
        form_class (class): 用于验证请求参数的 Django 表单类。

    Returns:
        function: 一个包装后的函数，在表单验证成功时执行视图函数；
                  若验证失败，则返回错误响应。

    Example:
        @form_validator(MyForm)
        def my_view(request, *args, **kwargs):
            # 通过 request.form 访问验证后的表单数据
            return some_response
    """
    def decorator(view_func):
        @wraps(view_func)
        def _validate_form(request, *args, **kwargs):
            form = form_class(request.params)
            if form is None:
                return view_func(request, *args, **kwargs)
            setattr(request, 'form', form)
            if not form.is_valid():
                print(form.errors)
                return http_response(status_code=ERRORCODE.PARAM_ERROR)
            return view_func(request, *args, **kwargs)
        return _validate_form
    return decorator


def api_sso_checker(allow_anonymous=False, method="GET"):
    """
    用户登陆验证装饰器，用于在执行视图函数之前验证用户登陆状态。

    Args:
        allow_anonymous: 是否允许匿名访问。
        method: 请求类型验证

    Returns:
        function: 一个包装后的函数，在验证成功时执行视图函数；
                  若验证失败，则返回错误响应。

    Example:
        @api_sso_checker(method="POST")
        def my_view(request, *args, **kwargs):
            return some_response
    """
    def decorator(view_func):
        @wraps(view_func)
        def authenticate(request, *args, **kwargs):
            try:
                if allow_anonymous:
                    return view_func(request, *args, **kwargs)
                if method and (request.method != method.upper()):
                    return http_response(status_code=ERRORCODE.METHOD_NOT_ALLOWED)
                token = request.GET.get("token")
                if not token:
                    return http_response(status_code=ERRORCODE.NOT_LOGIN)
                user_info = JWTAuth().jwt_decode(token)
                if not user_info:
                    return http_response(status_code=ERRORCODE.NOT_LOGIN)
                setattr(request, user_info.get("user_id"))
                return view_func(request, *args, **kwargs)
            except Exception:
                logger.error(traceback.format_exc())
                return http_response(status_code=ERRORCODE.UNKNOWN)
        return authenticate
    return decorator
