# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from app.manager.constants import GenderType, AccountPosition, PermissionType


class Manager(AbstractBaseUser):
    name_cn = models.CharField("账号", max_length=32, unique=True)
    name_sn = models.CharField("姓名", max_length=64, null=False, blank=True)
    mail = models.CharField("邮件", max_length=100, null=False, blank=True)
    gender = models.SmallIntegerField("性别", choices=GenderType.CHOICES, default=GenderType.MALE)
    birthday = models.DateField("生日", null=True)
    address = models.CharField("籍贯", max_length=128, null=True)
    id_card = models.CharField("身份证号码", max_length=128, null=True)
    phone = models.CharField(u'联系电话', max_length=32, null=True)
    department = models.CharField("部门", max_length=64, null=False, blank=True)
    is_active = models.BooleanField("有效", default=True)
    is_staff = models.BooleanField("是否员工", default=False)
    session_key = models.CharField(max_length=128, null=False, blank=True)
    expire_time = models.DateTimeField("session过期时间", null=True)
    position = models.SmallIntegerField("职位", choices=AccountPosition.CHOICES, default=AccountPosition.Creator)
    permission_setting = models.SmallIntegerField("权限设置", choices=PermissionType.CHOICES, default=PermissionType.ALL)
    creator_id = models.IntegerField("创建者", null=True)
    last_editor_id = models.IntegerField("最后修改者", null=True)
    created_time = models.DateTimeField("创建时间", auto_now_add=True, editable=False)
    last_update = models.DateTimeField("最后修改时间", auto_now=True, editable=False)
    USERNAME_FIELD = 'id'
