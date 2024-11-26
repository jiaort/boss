# -*- coding: utf-8 -*-

import random
import string

from django.conf import settings
from datetime import datetime, timedelta

from app.manager.models import Manager


# 登陆后缓存中记录信息
def do_login(response, manager):
    session_key = gen_random_code()
    expire_time = datetime.now() + timedelta(minutes=600)
    Manager.objects.filter(id=manager.id).update(session_key=session_key, expire_time=expire_time)
    response.set_cookie("session_id", session_key, max_age=36000, domain=settings.SESSION_COOKIE_DOMAIN)


def gen_random_code(length=32):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))

