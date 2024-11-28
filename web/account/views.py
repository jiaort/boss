from datetime import datetime
from django.conf import settings
from django.db.models import Count
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import logout

from utils.response import http_response
from utils.errorcode import ERRORCODE

from app.manager.constants import MANAGER_INFO_COOKIE_KEY
from app.manager.models import Manager

from web.decorators import render_admin, login_check
from web.manager.backend import do_login


@login_check()
def account_list_view(request):
    data = {
        'active_classes': ['.home-menu'],
    }
    return render_admin(request, 'account/list.html', data)
