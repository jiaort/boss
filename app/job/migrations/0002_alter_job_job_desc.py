# Generated by Django 3.2.23 on 2024-02-02 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_desc',
            field=models.TextField(verbose_name='职位描述'),
        ),
    ]