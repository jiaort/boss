# -*- coding: utf-8 -*-


class GenderType(object):
    Unknown = 0
    Male = 1
    Female = 2

    CHOICES = (
        (Unknown, u"未知"),
        (Male, u"男"),
        (Female, u"女"),
    )


USER_INFO_COOKIE_KEY = "user_info"
