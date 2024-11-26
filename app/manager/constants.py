# -*- coding: utf-8 -*-

MANAGER_INFO_COOKIE_KEY = "manager_info"


class EntityType(object):
    ACCOUNT = 1
    GROUP = 2
    BUSINESS = 3


class ContactKind(object):
    Mobile = 1
    Email = 2

    CHOICES = (
        (Mobile, "手机"),
        (Email, "邮箱"),
    )


class CodeType(object):
    Company = 5
    Brand = 6
    Address = 7


class CaptchaType(object):
    """
    图片验证码类型
    """
    Register = 1
    Login = 2
    ForgotPasswd = 3
    ChangeMobile = 4
    ChangeMobileVerify = 5


class AccountPosition(object):
    Creator = 1
    Employee = 10

    CHOICES = (
        (Creator, "创建者"),
        (Employee, "员工"),
    )


class PermissionType(object):
    ALL = 1
    PART = 2
    NOT_OPEN = 3

    CHOICES = (
        (ALL, "所有权限"),
        (PART, "部分权限"),
        (NOT_OPEN, "不开放"),
    )


class GenderType(object):
    MALE = 1
    FEMALE = 2

    CHOICES = (
        (MALE, "男"),
        (FEMALE, "女"),
    )
