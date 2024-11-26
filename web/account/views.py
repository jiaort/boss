# -*- coding:utf-8 -*-

from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from utils.paginater import paginate
from utils.common import form_error
from utils.logger.syslogger import SysLogger

from web.decorators import render_admin, login_check

from app.account.models import Resume
from app.job.constants import Education

from web.account.forms import ResumeForm


@login_check()
def list_view(request):
    form = ResumeForm(request.GET)
    if not form.is_valid():
        messages.error(request, "</br>".join(form_error(form)), 'danger')
        return HttpResponseRedirect(reverse('resume_list'))

    resume_queryset, total = paginate([], request.GET.get('page') or 1)

    data = {
        'active_classes': ['.resume-menu'],
        'total': total,
        'resume_list': resume_queryset,
        'form': form,
    }
    try:
        name = form.cleaned_data.get('name')
        query = Q()
        if name:
            query &= Q(name__contains=name)
        resume_queryset = Resume.objects.filter(query).order_by('-id')
        resume_queryset, total = paginate(resume_queryset, request.GET.get('page') or 1)

        for item in resume_queryset:
            item.education = Education.DICT.get(item.education)
            if item.file_applicant:
                item.file_applicant = item.file_applicant.split(',')

        data['resume_list'] = resume_queryset
        data['total'] = total
    except Exception as ex:
        SysLogger.exception(ex, request)
        messages.error(request, '系统异常，请重试', 'danger')
        return render_admin(request, 'account/resume-list.html', data)

    return render_admin(request, 'account/resume-list.html', data)
