class Status:
    UBREGISTERED = 0
    REGISTERED = 1

    CHOICES = (
        (UBREGISTERED, u"未登记"),
        (REGISTERED, u"登记"),
    )

    DICT = dict(CHOICES)


class Gender:
    MALE = 1
    FEMALE = 2

    CHOICES = (
        (MALE, u"男"),
        (FEMALE, u"女"),
    )
