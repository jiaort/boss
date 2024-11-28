from app.account.models import Account
from utils.request_client import RequestClient


def wx_code_login(code):
    """第三方登录

    code -- 微信授权code
    return -- User, STATUS_CODE"""
    params = {
        "appid": "wx26dd37776ee9f17f",
        "secret": "b00201d207b57c4885fbb137301a50e5",
        "grant_type": "authorization_code",
        "code": code,
    }
    resp = RequestClient.query(url="https://api.weixin.qq.com/sns/jscode2session", method="GET", params=params)

    if not resp or resp.status_code != 200:
        return None
    data = resp.json()
    openid = data.get("openid")
    if not openid:
        return None

    user = Account.objects.filter(auth_id=openid).first()
    if not user:
        user = Account.objects.create(
            auth_id=openid,
        )
    return user
