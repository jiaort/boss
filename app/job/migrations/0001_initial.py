# Generated by Django 3.2.23 on 2024-02-02 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100, verbose_name='职位名称')),
                ('function_type', models.SmallIntegerField(choices=[(1, '技术类'), (2, '职能类'), (3, '销售类'), (4, '产品类'), (5, '运营类'), (6, '其他')], default=1, verbose_name='职能类型')),
                ('job_type', models.SmallIntegerField(choices=[(0, '默认'), (1, '开发'), (2, '系统测试')], default=0, null=True, verbose_name='工作类型')),
                ('sub_job_type', models.SmallIntegerField(choices=[(0, '默认'), (1, '开发'), (2, '系统测试')], default=0, null=True, verbose_name='子工作类型')),
                ('applicant_type', models.SmallIntegerField(choices=[(1, '社会招聘'), (2, '校园招聘')], default=1, verbose_name='招聘类型')),
                ('work_place', models.SmallIntegerField(choices=[(1, '全国'), (2, '北京')], default=1, verbose_name='工作地点')),
                ('sub_work_place', models.SmallIntegerField(choices=[(1, '全国'), (2, '海淀区')], default=1, verbose_name='子工作地点')),
                ('salary', models.SmallIntegerField(choices=[(0, '不限'), (1, '3000以下'), (2, '3000-5000'), (3, '5000-10000'), (4, '10000-20000'), (5, '20000-50000'), (6, '50000以上')], default=0, verbose_name='薪资待遇')),
                ('education', models.SmallIntegerField(choices=[(1, '其他'), (2, '初中'), (3, '高中'), (4, '中技'), (5, '中专'), (6, '大专'), (7, '本科'), (8, '硕士'), (9, '博士')], default=None, null=True, verbose_name='学历要求')),
                ('number', models.IntegerField(default=0, verbose_name='招聘人数')),
                ('experience', models.SmallIntegerField(choices=[(1, '社会招聘'), (2, '校园招聘')], default=1, verbose_name='工作经验')),
                ('email', models.CharField(max_length=200, verbose_name='投递邮箱')),
                ('job_inner_id', models.CharField(max_length=200, null=True, verbose_name='企业内部职位ID')),
                ('job_desc', models.CharField(max_length=10240, verbose_name='职位描述')),
                ('owner', models.IntegerField(null=True, verbose_name='负责人')),
                ('owner_name', models.CharField(max_length=64, null=True, verbose_name='负责人姓名')),
                ('channel', models.SmallIntegerField(choices=[(1, '所有'), (2, '微信'), (3, '互联网')], default=2, null=True, verbose_name='发布渠道')),
                ('status', models.SmallIntegerField(choices=[(1, '进行中'), (2, '已暂停'), (3, '已完成'), (4, '已取消')], default=1, verbose_name='职位状态')),
                ('publish', models.SmallIntegerField(choices=[(0, '未发布'), (1, '已发布')], default=0, verbose_name='发布状态')),
                ('tag', models.BooleanField(default=False, verbose_name='热招')),
                ('creator_id', models.IntegerField(null=True, verbose_name='创建者')),
                ('last_editor_id', models.IntegerField(null=True, verbose_name='最后修改者')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
            ],
        ),
    ]