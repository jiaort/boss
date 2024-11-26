#!/usr/bin/env python
# -*- coding: utf-8 -*-


class JobStatus(object):
    Processing = 1
    Paused = 2
    Completed = 3
    Cancelled = 4

    CHOICES = (
        (Processing, u"进行中"),
        (Paused, u"已暂停"),
        (Completed, u"已完成"),
        (Cancelled, u"已取消"),
    )

    DICT = dict(CHOICES)


class PublishStatus(object):
    Unpublished = 0
    Published = 1

    CHOICES = (
        (Unpublished, u"未发布"),
        (Published, u"已发布"),
    )

    DICT = dict(CHOICES)


class PublishChannel(object):
    All = 1
    WeiXin = 2
    WWW = 3

    CHOICES = (
        (All, u"所有"),
        (WeiXin, u"微信"),
        (WWW, u"互联网"),
    )

    DICT = dict(CHOICES)


class FunctionType(object):
    Tech = 1
    Function = 2
    Sales = 3
    Product = 4
    Operation = 5
    Other = 6

    CHOICES = (
        (Tech, u"技术类"),
        (Function, u"职能类"),
        (Sales, u"销售类"),
        (Product, u"产品类"),
        (Operation, u"运营类"),
        (Other, u"其他"),
    )

    DICT = dict(CHOICES)


class JobType(object):
    Default = 0
    Development = 1
    Test = 2

    CHOICES = (
        (Default, u"默认"),
        (Development, u"开发"),
        (Test, u"系统测试"),
    )

    DICT = dict(CHOICES)


class SubJobType(object):
    Default = 0
    Development = 1
    Test = 2

    CHOICES = (
        (Default, u"默认"),
        (Development, u"开发"),
        (Test, u"系统测试"),
    )

    DICT = dict(CHOICES)


class WorkPlace(object):
    All = 1
    Beijing = 2

    CHOICES = (
        (All, u"全国"),
        (Beijing, u"北京"),
    )

    DICT = dict(CHOICES)


class SubWorkPlace(object):
    All = 1
    HaiDian = 2

    CHOICES = (
        (All, u"全国"),
        (HaiDian, u"海淀区"),
    )

    DICT = dict(CHOICES)


class ApplicantType(object):
    Social = 1
    Campus = 2

    CHOICES = (
        (Social, u"社会招聘"),
        (Campus, u"校园招聘"),
    )

    DICT = dict(CHOICES)


class Education(object):
    Other = 1
    Junior = 2
    Senior = 3
    Technology = 4
    Middle = 5
    JuniorCollege = 6
    Undergraduate = 7
    Master = 8
    Doctor = 9

    CHOICES = (
        (Other, u"其他"),
        (Junior, u"初中"),
        (Senior, u"高中"),
        (Technology, u"中技"),
        (Middle, u"中专"),
        (JuniorCollege, u"大专"),
        (Undergraduate, u"本科"),
        (Master, u"硕士"),
        (Doctor, u"博士"),
    )

    DICT = dict(CHOICES)


class EMAIL(object):
    Company = 1
    Hr = 2

    CHOICES = (
        (Company, u"HR_inform@cmgos.com"),
        (Hr, u"mary@cmgos.com"),
    )

    CHOICES_LIST = [i[1] for i in CHOICES]

    DICT = dict(CHOICES)


class Salary(object):
    NoShow = 0
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6

    CHOICES = (
        (NoShow, u"不限"),
        (One, u"3000以下"),
        (Two, u"3000-5000"),
        (Three, u"5000-10000"),
        (Four, u"10000-20000"),
        (Five, u"20000-50000"),
        (Six, u"50000以上"),
    )

    DICT = dict(CHOICES)


class Experience(object):
    No = 0
    One = 1
    Two = 2
    Tree = 3
    Four = 4
    Five = 5

    CHOICES = (
        (No, u"经验不限"),
        (One, u"1年以内"),
        (Two, u"1-3年"),
        (Tree, u"3-5年"),
        (Four, u"5-10年"),
        (Five, u"10年以上"),
    )

    DICT = dict(CHOICES)
