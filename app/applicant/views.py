# -*- coding:utf-8 -*-
from django.db.models import Q

from utils.decorators import request_checker
from utils.email_client import SendEmailClient
from utils.errorcode import ERRORCODE
from utils.paginater import paginate
from utils.response import http_response
from utils.common import form_error

from app.applicant.forms import ApplicantForm
from app.applicant.models import Applicant
from app.account.models import Resume
from app.job.constants import *


@request_checker()
def applicant_list_view(request):
    """
    申请列表
    """
    user_id = request.user.id

    query = Q(account_id=user_id)
    applicant_queryset = Applicant.objects.select_related().filter(query)
    applicant_queryset, total = paginate(applicant_queryset, request.GET.get('page') or 1)

    job_list = []
    for item in applicant_queryset:
        job_list.append({
            'id': item.job.id,
            'job_title': item.job.job_title,
            'function_type': FunctionType.DICT.get(item.job.function_type),
            # 'job_type': JobType.DICT.get(item.job.job_type),
            # 'sub_job_type': JobType.DICT.get(item.job.sub_job_type),
            'applicant_type': ApplicantType.DICT.get(item.job.applicant_type),
            'work_place': WorkPlace.DICT.get(item.job.work_place),
            'sub_work_place': SubWorkPlace.DICT.get(item.job.sub_work_place),
            # 'salary': Salary.DICT.get(item.job.salary),
            # 'education': Education.DICT.get(item.job.education),
            # 'number': item.job.number,
            # 'experience': Experience.DICT.get(item.job.experience),
            # 'email': EMAIL.DICT.get(item.job.email),
            # 'job_inner_id': item.job.job_inner_id,
            'job_desc': item.job.job_desc,
            # 'owner': item.job.owner,
            # 'owner_name': item.job.owner_name,
            # 'channel': PublishChannel.DICT.get(item.job.channel),
            # 'status': JobStatus.DICT.get(item.job.status),
            'tag': item.job.tag,
            # 'creator_id': item.job.creator_id,
            # 'last_editor_id': item.job.last_editor_id,
            'created_time': item.job.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            'last_update': item.job.last_update.strftime('%Y-%m-%d %H:%M:%S'),
        })

    context = {
        'function_type': FunctionType.DICT,
        'work_place': WorkPlace.DICT,
        'job_list': job_list,
    }

    return http_response(status_code=ERRORCODE.SUCCESS, context=context)


@request_checker(method='POST')
def applicant_view(request):
    """
    申请职位
    """
    user_id = request.user.id

    form = ApplicantForm(request.POST)
    if not form.is_valid():
        return http_response(status_code=ERRORCODE.PARAM_ERROR, msg_cn="</br>".join(form_error(form)))

    job_id = form.cleaned_data.get('job_id')
    applicant = Applicant.objects.filter(job_id=job_id, account_id=user_id)
    if applicant:
        return http_response(status_code=ERRORCODE.USER_REPEAT)

    # 创建申请信息
    data = form.cleaned_data
    data['account_id'] = user_id

    applicant = Applicant.objects.create(**data)

    # 更新微简历信息
    resume_dict = dict(
        name=form.cleaned_data.get('name'),
        education=form.cleaned_data.get('education'),
        school=form.cleaned_data.get('school'),
        position=form.cleaned_data.get('position'),
    )

    Resume.objects.filter(account_id=user_id).update(**resume_dict)
    receivers = [EMAIL.DICT.get(item) for item in eval(applicant.job.email)]
    subject = f"""{form.cleaned_data.get('name')} | {form.cleaned_data.get('experience')}年, 应聘 {applicant.job.job_title} | {WorkPlace.DICT.get(applicant.job.work_place)}-{WorkPlace.DICT.get(applicant.job.sub_work_place)}"""
    content = f"""
                <h3>基本信息</h3>
                <p><strong>姓名：</strong>{applicant.name}</p>
                <p><strong>邮箱：</strong>{applicant.email}</p>
                <p><strong>电话：</strong>{applicant.mobile}</p>
                <h3>教育经历</h3>
                <p><strong>最高学历：</strong>{Education.DICT.get(int(applicant.education))}</p>
                <p><strong>毕业院校：</strong>{applicant.school}</p>
                <p><strong>所学专业：</strong>{applicant.profession}</p>
                <h3>工作经历</h3>
                <p><strong>当前公司：</strong>{applicant.company}</p>
                <p><strong>当前职位：</strong>{applicant.position}</p>
                <p><strong>总工作年限：</strong>{applicant.experience}</p>
                """
    attachments = applicant.file_applicant.split(',') if applicant.file_applicant else []
    SendEmailClient.send_email_sync(receivers=receivers, subject=subject, content=content, attachments=attachments)

    return http_response(status_code=ERRORCODE.SUCCESS)
