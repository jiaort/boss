# -*- coding: utf-8 -*-

from django import forms


class JobForm(forms.Form):
    """新建/编辑职位"""
    job_title = forms.CharField(label=u'职位名称', max_length=200)
    function_type = forms.IntegerField(label=u"职能类型")
    # job_type = forms.IntegerField(label=u"工作类型", required=False)
    # sub_job_type = forms.IntegerField(label=u"子工作类型", required=False)
    applicant_type = forms.IntegerField(label=u"招聘类型")
    work_place = forms.IntegerField(label=u"工作地点")
    sub_work_place = forms.IntegerField(label=u"子工作地点")
    # salary = forms.IntegerField(label=u"薪资待遇", required=False)
    education = forms.IntegerField(label=u"学历要求")
    number = forms.IntegerField(label=u"招聘人数")
    experience = forms.IntegerField(label=u"工作经验")
    email = forms.IntegerField(label=u'投递邮箱')
    job_inner_id = forms.CharField(label=u'企业内部职位ID', max_length=200, required=False)
    job_desc = forms.CharField(label=u'职位描述', widget=forms.Textarea)
    owner = forms.IntegerField(label=u"负责人", required=False)
    owner_name = forms.CharField(label=u'负责人姓名', max_length=64, required=False)
    # channel = forms.IntegerField(label=u"发布渠道", required=False)
    status = forms.IntegerField(label=u"职位状态")
    publish = forms.IntegerField(label=u"发布状态")


class JobListForm(forms.Form):
    job_title = forms.CharField(label=u'职位名称', max_length=200, required=False)
    function_type = forms.IntegerField(label=u"职能类型", required=False)
    status = forms.IntegerField(label=u"职位状态", required=False)
    status_order = forms.IntegerField(label=u"职位状态排序", required=False)
    publish = forms.IntegerField(label=u"发布状态", required=False)
    publish_order = forms.IntegerField(label=u"发布状态排序", required=False)
