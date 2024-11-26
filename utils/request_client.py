import requests

MAX_CONSUMING_TIME = 500  # 单位ms


class RequestClient(object):
    """
    封装http requests： 记录日志、重试机制、保护机制

    调用方法： RequestClient.query(url=url)
    """
    _request_session = requests.Session()     # 带有会话的请求,可以使用连接池

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

    @classmethod
    def query(cls, url, method="POST", params=None, data={}, files={}, timeout=3, retry=1,
              headers=None, add_sep_headers=False, record_params=True, stream=False, **kwargs):
        """
            :params url: 要访问的url
            :param params: 参数In URL
            :param data: form-data数据
            :param files: POST a Multipart-Encoded File
            :param retry: 当失败时候，重试次数
            :params record_params 记录日志的时候是否需要将params/data你们的数据记录
            :return response or None
        """
        params = params if params else {}
        method = method.lower()
        times = 0
        response = None
        # get headers
        default_headers = cls._get_headers(add_sep_headers, headers)

        while times < retry:
            try:
                if kwargs.get('cert'):
                    # 带证书的请求使用requests session，如果两次使用不同证书，requests只使用第一次初始化时的证书，
                    # 所以这里如果使用了证书就不使用session
                    request_mode = requests
                else:
                    request_mode = cls._request_session
                response = getattr(request_mode, method)(url=url, params=params, data=data, headers=default_headers,
                                                         files=files, timeout=timeout, stream=stream, **kwargs)
                return response
            except Exception as exp:
                pass
        return response
