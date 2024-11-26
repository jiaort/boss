class SecretHierarchy:
    TOP_SECRET = 1
    CONFIDENTIAL = 2
    SECRET = 3
    INTERNAL = 4
    UNCLASSIFIED = 5

    CHOICES = (
        (TOP_SECRET, u"绝密"),
        (CONFIDENTIAL, u"机密"),
        (SECRET, u"秘密"),
        (INTERNAL, u"内部"),
        (UNCLASSIFIED, u"一般"),
    )

    DICT = dict(CHOICES)
