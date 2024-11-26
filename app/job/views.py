# -*- coding:utf-8 -*-
from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse
from docx import Document
from docx.shared import Inches

from utils.decorators import request_checker
from utils.errorcode import ERRORCODE
from utils.paginater import paginate
from utils.response import http_response
from utils.common import get_choice_id

from app.job.models import Job
from app.job.constants import *

from app.account.models import Favorite


@request_checker()
def job_list_view(request):
    user_id = request.user.id

    job_title = request.GET.get('job_title')
    function_type = request.GET.get('function_type')
    applicant_type = request.GET.get('applicant_type')
    work_place = request.GET.get('work_place')
    job_ids = request.GET.get('job_ids')

    query = Q(publish=PublishStatus.Published)
    if job_title:
        query &= Q(job_title__contains=job_title)
    if function_type:
        function_type = get_choice_id(FunctionType.CHOICES, function_type)
        query &= Q(function_type=function_type)
    if applicant_type:
        query &= Q(applicant_type=applicant_type)
    if work_place:
        work_place = work_place.split('-')
        if len(work_place) < 2:
            return http_response(status_code=ERRORCODE.PARAM_ERROR)

        work_place_id = get_choice_id(WorkPlace.CHOICES, work_place[0])
        sub_work_place_id = get_choice_id(SubWorkPlace.CHOICES, work_place[1])

        query &= Q(work_place=work_place_id) & Q(sub_work_place=sub_work_place_id)
    if job_ids:
        job_id_list = job_ids.split(',')
        query &= Q(id__in=job_id_list)

    job_queryset = Job.objects.filter(query)
    job_queryset, total = paginate(job_queryset, request.GET.get('page') or 1, request.GET.get('size') or 100)

    job_id_list = [item.id for item in job_queryset]

    favorite = Favorite.objects.filter(account_id=user_id, job_id__in=job_id_list)
    favorite_id_list = [item.job_id for item in favorite]

    job_list = []
    for item in job_queryset:
        job_list.append({
            'id': item.id,
            'job_title': item.job_title,
            'function_type': FunctionType.DICT.get(item.function_type),
            # 'job_type': JobType.DICT.get(item.job_type),
            # 'sub_job_type': JobType.DICT.get(item.sub_job_type),
            'applicant_type': ApplicantType.DICT.get(item.applicant_type),
            'work_place': WorkPlace.DICT.get(item.work_place) + '-' + SubWorkPlace.DICT.get(item.sub_work_place),
            # 'salary': Salary.DICT.get(item.salary),
            # 'education': Education.DICT.get(item.education),
            # 'number': item.number,
            # 'experience': Experience.DICT.get(item.experience),
            # 'email': EMAIL.DICT.get(item.email),
            # 'job_inner_id': item.job_inner_id,
            'job_desc': item.job_desc,
            # 'owner': item.owner,
            # 'owner_name': item.owner_name,
            # 'channel': PublishChannel.DICT.get(item.channel),
            # 'status': JobStatus.DICT.get(item.status),
            'tag': item.tag,
            'favorite': item.id in favorite_id_list,
            # 'creator_id': item.creator_id,
            # 'last_editor_id': item.last_editor_id,
            'created_time': item.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            'last_update': item.last_update.strftime('%Y-%m-%d %H:%M:%S'),
        })

    work_place_list = []
    job_queryset = Job.objects.filter(publish=PublishStatus.Published)
    for item in job_queryset:
        work_place_list.append(WorkPlace.DICT.get(item.work_place) + '-' + SubWorkPlace.DICT.get(item.sub_work_place))

    context = {
        'function_type': list(FunctionType.DICT.values()),
        'work_place': list(set(work_place_list)),
        'job_list': job_list,
    }

    return http_response(status_code=ERRORCODE.SUCCESS, context=context)


@request_checker()
def detail_view(request, job_id):
    query = Q(id=job_id)
    job_query = Job.objects.filter(query).first()

    job_info = {
        'id': job_query.id,
        'job_title': job_query.job_title,
        'function_type': FunctionType.DICT.get(job_query.function_type),
        # 'channel': job_query.channel,
        'applicant_type': ApplicantType.DICT.get(job_query.applicant_type),
        # 'job_type': job_query.job_type,
        # 'sub_job_type': job_query.sub_job_type,
        'work_place': WorkPlace.DICT.get(job_query.work_place) + '-' + SubWorkPlace.DICT.get(job_query.sub_work_place),
        # 'salary': job_query.salary,
        # 'education': job_query.education,
        # 'number': job_query.number,
        # 'experience': job_query.experience,
        # 'email': json.loads(job_query.email),
        # 'job_inner_id': job_query.job_inner_id,
        'job_desc': job_query.job_desc,
        # 'owner_name': job_query.owner_name,
        # 'status': job_query.status,
        'tag': job_query.tag,
        'created_time': job_query.created_time.strftime('%Y-%m-%d %H:%M:%S'),
        'last_update': job_query.last_update.strftime('%Y-%m-%d %H:%M:%S'),
    }

    context = {
        'job_info': job_info,
    }

    return http_response(status_code=ERRORCODE.SUCCESS, context=context)
