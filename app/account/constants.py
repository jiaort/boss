# -*- coding: utf-8 -*-


class GenderType(object):
    Unknown = 0
    Male = 1
    Female = 2

    CHOICES = (
        (Unknown, "未知"),
        (Male, "男"),
        (Female, "女"),
    )


USER_INFO_COOKIE_KEY = "user_info"
