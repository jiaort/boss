# -*- coding:utf-8 -*-
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
from utils.paginater import paginate
from utils.response import http_response
from utils.common import upload_file

from app.account.forms import ResumeForm
from app.account.models import Favorite, Resume
from app.job.constants import *


@request_checker()
def favorite_list_view(request):
    """
    收藏列表
    :param request:
    :return:
    """
    user_id = request.user.id
    query = Q(account_id=user_id)
    favorite_queryset = Favorite.objects.filter(query).order_by('-id')
    favorite_queryset, total = paginate(favorite_queryset, request.GET.get('page') or 1)

    job_list = []
    for item in favorite_queryset:
        job = item.job
        job_list.append({
            'id': job.id,
            'job_title': job.job_title,
            'function_type': FunctionType.DICT.get(job.function_type),
            # 'job_type': JobType.DICT.get(job.job_type),
            # 'sub_job_type': JobType.DICT.get(job.sub_job_type),
            # 'applicant_type': ApplicantType.DICT.get(job.applicant_type),
            'work_place': WorkPlace.DICT.get(job.work_place) + '-' + SubWorkPlace.DICT.get(job.sub_work_place),
            # 'sub_work_place': SubWorkPlace.DICT.get(job.sub_work_place),
            # 'salary': Salary.DICT.get(job.salary),
            # 'education': Education.DICT.get(job.education),
            # 'number': job.number,
            # 'experience': Experience.DICT.get(job.experience),
            # 'email': EMAIL.DICT.get(job.email),
            # 'job_inner_id': job.job_inner_id,
            'job_desc': job.job_desc,
            # 'owner': job.owner,
            # 'owner_name': job.owner_name,
            # 'channel': PublishChannel.DICT.get(job.channel),
            # 'status': JobStatus.DICT.get(job.status),
            'tag': job.tag,
            # 'creator_id': job.creator_id,
            # 'last_editor_id': job.last_editor_id,
            'created_time': job.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            # 'last_update': job.last_update.strftime('%Y-%m-%d %H:%M:%S'),
        })

    context = {
        'total': total,
        'job_list': job_list,
    }

    return http_response(status_code=ERRORCODE.SUCCESS, context=context)


@request_checker(method='POST')
def favorite_view(request):
    """
    收藏/取消收藏
    :param request:
    :return:
    """
    user_id = request.user.id
    job_id = request.POST.get('job_id')

    result = Favorite.objects.filter(account_id=user_id, job_id=job_id).delete()

    if result[0] == 0:
        Favorite.objects.create(
            account_id=user_id,
            job_id=job_id,
        )

    return http_response(status_code=ERRORCODE.SUCCESS)


@request_checker()
def resume_view(request):
    """
    微简历
    :param request:
    :return:
    """
    user_id = request.user.id

    resume = Resume.objects.filter(account_id=user_id).first()

    if resume:
        file_applicant_name = []
        if resume.file_applicant:
            file_applicant = resume.file_applicant.split(',')
            for item in file_applicant:
                file_applicant_name.append(item.split('_', 2)[-1])
        else:
            file_applicant = None
            file_applicant_name = None

        file_name = None
        if resume.file:
            file_name = resume.file.split('_', 2)[-1]

        resume_info = {
            'name': resume.name,
            'mobile': resume.mobile,
            'email': resume.email,
            'education': resume.education,
            'school': resume.school,
            'profession': resume.profession,
            'company': resume.company,
            'position': resume.position,
            'experience': resume.experience,
            'file': resume.file,
            'file_name': file_name,
            'file_applicant': file_applicant,
            'file_applicant_name': file_applicant_name,
        }

        context = {
            'education': Education.DICT,
            'resume_info': resume_info
        }

        return http_response(status_code=ERRORCODE.SUCCESS, context=context)
    else:
        context = {
            'education': Education.DICT,
        }
        return http_response(status_code=ERRORCODE.NOT_FOUND, context=context)


@request_checker(method='POST')
def edit_resume_view(request):
    """
    新建或编辑微简历
    :param request:
    :return:
    """
    user_id = request.user.id

    form = ResumeForm(request.POST)
    if not form.is_valid():
        return http_response(status_code=ERRORCODE.PARAM_ERROR)

    data = form.cleaned_data
    data['account_id'] = user_id

    if Resume.objects.filter(account_id=user_id).update(**data) < 1:
        Resume.objects.create(**data)

    return http_response(status_code=ERRORCODE.SUCCESS)


def upload_file_view(request):
    """
    上传附件简历
    :param request:
    :return:
    """
    user_id = request.user.id

    file = request.FILES.get('file')
    if not file:
        return http_response(status_code=ERRORCODE.PARAM_ERROR, msg_cn="请上传附件简历")

    result, file_path = upload_file(file, user_id)
    if not result:
        return http_response(status_code=ERRORCODE.FAILED, msg_cn="附件简历上传失败")

    context = {'file_path': file_path}

    return http_response(context=context, status_code=ERRORCODE.SUCCESS)


@request_checker(method='POST')
def upload_resume_view(request):
    """
    上传简历
    :param request:
    :return:
    """
    user_id = request.user.id

    file = request.FILES.get('file')
    if not file:
        return http_response(status_code=ERRORCODE.PARAM_ERROR, msg_cn="请上传附件简历")

    result, file_path = upload_file(file)
    if not result:
        return http_response(status_code=ERRORCODE.FAILED, msg_cn="附件简历上传失败")

    if Resume.objects.filter(account_id=user_id).update(file=file_path) < 1:
        Resume.objects.create(account_id=user_id, file=file_path)

    return http_response(status_code=ERRORCODE.SUCCESS)


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

    user, error = wx_code_login(request=request, code=code)
    if user:
        response = HttpResponseRedirect(next_url)
        return response
    else:
        # fixme 需要一个失败的跳转
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
