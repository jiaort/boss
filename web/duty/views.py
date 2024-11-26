# -*- coding:utf-8 -*-
import json

from django.db.models import Q, Count
from django.contrib import messages

from app.job.constants import *
from web.document.forms import JobListForm, JobForm
from app.job.models import Job
from app.applicant.models import Applicant
from utils.errorcode import ERRORCODE
from utils.paginater import paginate
from utils.response import http_response
from utils.common import form_error
from utils.logger.syslogger import SysLogger
from web.decorators import render_admin, login_check, login_check_ajax

@login_check()
def list_duty_view(request):
    form = JobListForm(request.GET)
    form.is_valid()
    job_queryset, total = paginate([], request.GET.get('page') or 1)

    job_status_count = [0, 0, 0, 0, 0]
    data = {
        'active_classes': ['.duty-menu'],
        'open_classes': [],
        'job_list': job_queryset,
        'total': total,
        'form': form,
        'job_status_count': job_status_count,
        'function_type_option': FunctionType.CHOICES,
        'job_status_option': JobStatus.CHOICES,
        'publish_status_option': PublishStatus.CHOICES,
    }
    try:
        query = Q()
        job_title = form.cleaned_data.get('job_title')
        function_type = form.cleaned_data.get('function_type')
        status = form.cleaned_data.get('status')
        publish = form.cleaned_data.get('publish')
        if job_title:
            query &= Q(job_title__contains=job_title)
        if function_type is not None:
            query &= Q(function_type=function_type)
        if status is not None:
            query &= Q(status=status)
        if publish is not None:
            query &= Q(publish=publish)

        job_queryset = Job.objects.filter(query)

        status_order = form.cleaned_data.get('status_order')
        publish_order = form.cleaned_data.get('publish_order')
        if not status_order and not publish_order:
            job_queryset = job_queryset.order_by('-id')

        if status_order == 1:
            job_queryset = job_queryset.order_by('status')
        elif status_order == 2:
            job_queryset = job_queryset.order_by('-status')

        if publish_order == 1:
            job_queryset = job_queryset.order_by('publish')
        elif publish_order == 2:
            job_queryset = job_queryset.order_by('-publish')

        job_queryset, total = paginate(job_queryset, request.GET.get('page') or 1)

        job_id_list = [item.id for item in job_queryset]

        applicant_stat = Applicant.objects.filter(job_id__in=job_id_list).values_list('job_id').annotate(Count('id'))
        applicant_stat_dict = {}
        for item in applicant_stat:
            applicant_stat_dict[item[0]] = item[1]

        for item in job_queryset:
            item.function_type = FunctionType.DICT.get(item.function_type)
            item.job_type = JobType.DICT.get(item.job_type)
            item.sub_job_type = JobType.DICT.get(item.sub_job_type)
            item.applicant_type = ApplicantType.DICT.get(item.applicant_type)
            item.work_place = WorkPlace.DICT.get(item.work_place) + '-' + SubWorkPlace.DICT.get(item.sub_work_place)
            item.salary = Salary.DICT.get(item.salary)
            item.education = Education.DICT.get(item.education)
            item.experience = Experience.DICT.get(item.experience)
            item.email = EMAIL.DICT.get(item.email)
            item.count = applicant_stat_dict.get(item.id) or 0
            item.channel = PublishChannel.DICT.get(item.channel)
            item.status = JobStatus.DICT.get(item.status)
            item.publish = PublishStatus.DICT.get(item.publish)
            # item.created_time = item.created_time.strftime('%Y-%m-%d %H:%M:%S')
            # item.last_update = item.last_update.strftime('%Y-%m-%d %H:%M:%S')

        data['job_list'] = job_queryset
        data['total'] = total

        job_annotate = Job.objects.values("status").annotate(count=Count("id"))

        total_status_count = 0
        for item in job_annotate:
            if item["status"] == JobStatus.Processing:
                job_status_count[1] = item["count"]
            elif item["status"] == JobStatus.Paused:
                job_status_count[2] = item["count"]
            elif item["status"] == JobStatus.Completed:
                job_status_count[3] = item["count"]
            elif item["status"] == JobStatus.Cancelled:
                job_status_count[4] = item["count"]
            total_status_count += item["count"]

        job_status_count[0] = total_status_count
        data['job_status_count'] = job_status_count
    except Exception as ex:
        SysLogger.exception(ex, request)
        messages.error(request, '系统异常，请重试', 'danger')
        return render_admin(request, 'duty/list.html', data)

    return render_admin(request, 'duty/list.html', data)



@login_check_ajax()
def get_duty_view(request, duty_id):
    print(duty_id)
    try:
        query = Q(id=duty_id)
        job_query = Job.objects.filter(query).first()

        content = {
            'id': job_query.id,
            'job_title': job_query.job_title,
            'job_status': job_query.status,
            'publish_status': job_query.publish,
            'channel': job_query.channel,
            'function_type': job_query.function_type,
            'applicant_type': job_query.applicant_type,
            'job_type': job_query.job_type,
            'sub_job_type': job_query.sub_job_type,
            'work_place': job_query.work_place,
            'sub_work_place': job_query.sub_work_place,
            'salary': job_query.salary,
            'education': job_query.education,
            'number': job_query.number,
            'experience': job_query.experience,
            'email': json.loads(job_query.email),
            'job_inner_id': job_query.job_inner_id,
            'job_desc': job_query.job_desc,
            'owner_name': job_query.owner_name,
            'created_time': job_query.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            'last_update': job_query.last_update.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return http_response(status_code=ERRORCODE.SUCCESS, context={"content": content})
    except Exception as ex:
        SysLogger.exception(ex, request)
        return http_response(status_code=ERRORCODE.FAILED)


@login_check_ajax()
def create_duty_view(request, duty_id=None):
    form = JobForm(request.POST)
    if not form.is_valid():
        return http_response(status_code=ERRORCODE.PARAM_ERROR, msg_cn="</br>".join(form_error(form)))

    try:
        data = form.cleaned_data
        email_list = request.POST.getlist('email')
        data['email'] = json.dumps([int(i) for i in email_list])

        if duty_id:
            Job.objects.filter(id=duty_id).update(**data)
        else:
            Job.objects.create(**data)
        return http_response(status_code=ERRORCODE.SUCCESS)
    except Exception as ex:
        SysLogger.exception(ex, request)
        return http_response(status_code=ERRORCODE.FAILED)
