# Generated by Django 3.2.23 on 2024-02-02 14:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('job', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='应聘者姓名')),
                ('mobile', models.CharField(max_length=16, verbose_name='电话')),
                ('email', models.CharField(max_length=128, verbose_name='邮箱')),
                ('source', models.SmallIntegerField(choices=[(1, '所有'), (2, '微信'), (3, '互联网')], default=1, verbose_name='来源')),
                ('education', models.SmallIntegerField(choices=[(1, '其他'), (2, '初中'), (3, '高中'), (4, '中技'), (5, '中专'), (6, '大专'), (7, '本科'), (8, '硕士'), (9, '博士')], default=1, verbose_name='学历')),
                ('school', models.CharField(max_length=200, verbose_name='毕业院校')),
                ('profession', models.CharField(max_length=200, verbose_name='所学专业')),
                ('company', models.CharField(max_length=200, verbose_name='当前公司')),
                ('position', models.CharField(max_length=200, verbose_name='当前职位')),
                ('experience', models.CharField(max_length=50, verbose_name='工作年限')),
                ('file_applicant', models.CharField(blank=True, max_length=2000, null=True, verbose_name='申请附件')),
                ('read', models.BooleanField(default=False, verbose_name='读取状态')),
                ('status', models.SmallIntegerField(choices=[(0, '待处理'), (1, '合适'), (2, '不合适'), (3, '待定')], default=0, verbose_name='处理状态')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('account', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='job.job')),
            ],
        ),
    ]
