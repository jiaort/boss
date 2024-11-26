# -*- coding: utf-8 -*-

from app.applicant.models import Applicant


def applicant_count(job_id_list):
    count = Applicant.objects.filter(job_id__in=job_id_list).count()
    return count
