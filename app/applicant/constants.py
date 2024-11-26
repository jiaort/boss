# -*- coding: utf-8 -*-


class Status(object):
    New = 0
    Suitable = 1
    Inappropriate = 2
    Tobe = 3

    CHOICES = (
        (New, u"待处理"),
        (Suitable, u"合适"),
        (Inappropriate, u"不合适"),
        (Tobe, u"待定"),
    )

    DICT = dict(CHOICES)


class Source(object):
    All = 1
    WeiXin = 2
    WWW = 3

    CHOICES = (
        (All, u"所有"),
        (WeiXin, u"微信"),
        (WWW, u"互联网"),
    )

    DICT = dict(CHOICES)
