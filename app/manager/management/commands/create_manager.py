import getpass
import hashlib

from django.core.management import BaseCommand
from django.utils.termcolors import colorize

from app.manager.models import Manager


class Command(BaseCommand):

    def create_superuser(self):
        print(colorize("创建超级管理员", fg="cyan"))

        username = ''
        input_username = input(colorize("请输入用户名:", fg="yellow"))
        if input_username:
            username = input_username
        else:
            print(colorize("您没有输入,已结束流程.", fg="red"))
            exit()
        passwd1 = passwd2 = None

        while not (passwd1 and passwd2 and len(passwd1) >= 8 and passwd1 == passwd2):
            passwd1 = getpass.getpass(colorize("请输入密码(8位以上):", fg="yellow"))
            if not passwd1:
                continue
            passwd2 = getpass.getpass(colorize("请再次输入密码(8位以上):", fg="yellow"))

        manager = Manager.objects.create(
            name_cn=username,
            name_sn=username,
            is_staff=True
        )
        # md5_password = hashlib.md5(passwd2.encode(encoding='UTF-8')).hexdigest()
        manager.set_password(passwd2)
        manager.save()
        print(colorize("超级管理员账号创建成功", fg="green"))

    def handle(self, *args, **options):
        try:
            self.create_superuser()

        except Exception as exp:
            print(exp)
