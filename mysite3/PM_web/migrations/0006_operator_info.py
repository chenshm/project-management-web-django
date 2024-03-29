# Generated by Django 2.2 on 2019-05-28 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PM_web', '0005_auto_20190527_1454'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operator_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(choices=[('京', '北京市'), ('津', '天津市')], default='京', max_length=32, verbose_name='运营商所属省份')),
                ('city', models.CharField(default='', max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('priority', models.CharField(choices=[('1', '第一优先级'), ('2', '第二优先级'), ('3', '第三优先级')], default=2, max_length=12)),
                ('total_user', models.IntegerField(default=0)),
                ('total_boot_user', models.IntegerField(default=0)),
                ('total_incoming', models.IntegerField(default=0)),
            ],
        ),
    ]
