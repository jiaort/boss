# -*- coding: utf-8 -*-

from django.db import models

from app.job.constants import JobStatus, PublishChannel, JobType, SubJobType, WorkPlace, SubWorkPlace, ApplicantType, \
    Education, Salary, PublishStatus, FunctionType


class Job(models.Model):
    job_title = models.CharField(u"职位名称", max_length=100)
    function_type = models.SmallIntegerField(u"职能类型", choices=FunctionType.CHOICES, default=FunctionType.Tech)
    job_type = models.SmallIntegerField(u"工作类型", choices=JobType.CHOICES, default=JobType.Default, null=True)
    sub_job_type = models.SmallIntegerField(u"子工作类型", choices=SubJobType.CHOICES, default=SubJobType.Default, null=True)
    applicant_type = models.SmallIntegerField(u"招聘类型", choices=ApplicantType.CHOICES, default=ApplicantType.Social)
    work_place = models.SmallIntegerField(u"工作地点", choices=WorkPlace.CHOICES, default=WorkPlace.All)
    sub_work_place = models.SmallIntegerField(u"子工作地点", choices=SubWorkPlace.CHOICES, default=SubWorkPlace.All)
    salary = models.SmallIntegerField(u"薪资待遇", choices=Salary.CHOICES, default=Salary.NoShow)
    education = models.SmallIntegerField(u"学历要求", choices=Education.CHOICES, default=None, null=True)
    number = models.IntegerField("招聘人数", default=0)
    experience = models.SmallIntegerField(u"工作经验", choices=ApplicantType.CHOICES, default=ApplicantType.Social)
    email = models.CharField(u"投递邮箱", max_length=200)
    job_inner_id = models.CharField(u"企业内部职位ID", max_length=200, null=True)
    job_desc = models.TextField(u"职位描述")
    owner = models.IntegerField("负责人", null=True)
    owner_name = models.CharField("负责人姓名", max_length=64, null=True)
    channel = models.SmallIntegerField(u"发布渠道", choices=PublishChannel.CHOICES, default=PublishChannel.WeiXin, null=True)
    status = models.SmallIntegerField(u"职位状态", choices=JobStatus.CHOICES, default=JobStatus.Processing)
    publish = models.SmallIntegerField(u"发布状态", choices=PublishStatus.CHOICES, default=PublishStatus.Unpublished)
    tag = models.BooleanField(u"热招", default=False)
    creator_id = models.IntegerField("创建者", null=True)
    last_editor_id = models.IntegerField("最后修改者", null=True)
    created_time = models.DateTimeField(u"创建时间", auto_now_add=True, editable=False)
    last_update = models.DateTimeField(u"最后修改时间", auto_now=True, editable=False)
