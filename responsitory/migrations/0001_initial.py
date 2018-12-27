# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-10-04 07:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import responsitory.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article2Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'Article2Tag',
            },
        ),
        migrations.CreateModel(
            name='ArticleInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='文章标题')),
                ('summary', models.TextField(null=True, verbose_name='简介')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('detail', models.TextField(verbose_name='文章内容')),
                ('index_type', models.IntegerField(choices=[(1, '技术'), (2, '新闻'), (3, '其他')], default=1, help_text='固定分类', verbose_name='总分类')),
                ('read_num', models.IntegerField(default=0, verbose_name='阅读量')),
            ],
            options={
                'verbose_name_plural': '文章表',
                'db_table': 'ArticleInfo',
            },
        ),
        migrations.CreateModel(
            name='BillInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=32, verbose_name='唯一标志')),
                ('title', models.CharField(max_length=128, verbose_name='标题')),
                ('detail', models.TextField(verbose_name='详细')),
                ('submit_time', models.DateTimeField(auto_now_add=True, verbose_name='提交时间')),
                ('status', models.IntegerField(choices=[(1, '未处理'), (2, '待处理'), (3, '已处理')], verbose_name='状态')),
                ('solution', models.TextField(blank=True, null=True, verbose_name='解决办法')),
                ('evaluate', models.TextField(blank=True, null=True, verbose_name='评价信息')),
                ('handle_time', models.DateTimeField(blank=True, null=True, verbose_name='处理时间')),
            ],
            options={
                'verbose_name_plural': '保障信息表',
                'db_table': 'BillInfo',
            },
        ),
        migrations.CreateModel(
            name='BlogInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surfix', models.CharField(max_length=16, unique=True, verbose_name='url后缀')),
                ('signature', models.CharField(max_length=30, verbose_name='个性签名')),
                ('title', models.CharField(max_length=16, verbose_name='标题')),
            ],
            options={
                'verbose_name_plural': '个人博客表',
                'db_table': 'BlogInfo',
            },
        ),
        migrations.CreateModel(
            name='CategoryInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=16, verbose_name='种类名')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='responsitory.BlogInfo', verbose_name='所属博客')),
            ],
            options={
                'verbose_name_plural': '种类表',
                'db_table': 'CategoryInfo',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=12, verbose_name='市名')),
            ],
        ),
        migrations.CreateModel(
            name='CommentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('detail', models.TextField(verbose_name='评论详细')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='responsitory.ArticleInfo', verbose_name='所属文章')),
                ('comment_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='responsitory.CommentInfo', verbose_name='父评论')),
            ],
            options={
                'verbose_name_plural': '评论表',
                'db_table': 'CommentInfo',
            },
        ),
        migrations.CreateModel(
            name='CSSInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=16, verbose_name='主题名')),
                ('file', models.FileField(upload_to='css', verbose_name='css文件')),
            ],
        ),
        migrations.CreateModel(
            name='EvaluateInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField(choices=[(1, '赞'), (2, '踩')], verbose_name='动作')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='responsitory.ArticleInfo', verbose_name='所属文章')),
            ],
            options={
                'verbose_name_plural': '踩赞表',
                'db_table': 'EvaluateInfo',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=12, verbose_name='省份名')),
            ],
        ),
        migrations.CreateModel(
            name='Star2Fans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'Star2Fans',
            },
        ),
        migrations.CreateModel(
            name='StudyPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='技术名字')),
            ],
        ),
        migrations.CreateModel(
            name='TagInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=8, verbose_name='博客标题')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='responsitory.BlogInfo', verbose_name='所属博客')),
            ],
            options={
                'verbose_name_plural': '标签表',
                'db_table': 'TagInfo',
            },
        ),
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=12, verbose_name='镇名')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='responsitory.City', verbose_name='所属市')),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', models.CharField(blank=True, max_length=128, null=True, verbose_name='个性签名')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('location_detail', models.CharField(blank=True, max_length=128, null=True, verbose_name='详细住址')),
                ('interest', models.ManyToManyField(blank=True, null=True, to='responsitory.StudyPoint', verbose_name='兴趣技术点')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='responsitory.Town', verbose_name='所在地')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=16, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('email', models.EmailField(max_length=32, unique=True, verbose_name='邮箱')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='手机号码')),
                ('img', models.ImageField(default='head/default.jpg', upload_to=responsitory.models.upload_to, verbose_name='用户头像')),
                ('enroll_date', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('detail', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='responsitory.UserDetail', verbose_name='用户详细信息')),
            ],
            options={
                'verbose_name_plural': '用户表',
                'db_table': 'UserInfo',
            },
        ),
        migrations.AddField(
            model_name='star2fans',
            name='fans_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fans', to='responsitory.UserInfo', verbose_name='粉丝'),
        ),
        migrations.AddField(
            model_name='star2fans',
            name='star_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stars', to='responsitory.UserInfo', verbose_name='被粉者'),
        ),
        migrations.AddField(
            model_name='evaluateinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='responsitory.UserInfo', verbose_name='动作所属用户'),
        ),
        migrations.AddField(
            model_name='commentinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='responsitory.UserInfo', verbose_name='所属用户'),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='responsitory.Province', verbose_name='所属省份'),
        ),
        migrations.AddField(
            model_name='bloginfo',
            name='css',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='responsitory.CSSInfo', verbose_name='主题样式'),
        ),
        migrations.AddField(
            model_name='bloginfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='responsitory.UserInfo', verbose_name='所属用户'),
        ),
        migrations.AddField(
            model_name='billinfo',
            name='handler',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='handler_bill', to='responsitory.UserInfo', verbose_name='处理者'),
        ),
        migrations.AddField(
            model_name='billinfo',
            name='submitter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitter_bill', to='responsitory.UserInfo', verbose_name='提交者'),
        ),
        migrations.AddField(
            model_name='articleinfo',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='responsitory.BlogInfo', verbose_name='所属博客'),
        ),
        migrations.AddField(
            model_name='articleinfo',
            name='category',
            field=models.ForeignKey(blank=True, help_text='用户自定义分类', null=True, on_delete=django.db.models.deletion.CASCADE, to='responsitory.CategoryInfo', verbose_name='种类'),
        ),
        migrations.AddField(
            model_name='article2tag',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='responsitory.ArticleInfo', verbose_name='所属文章'),
        ),
        migrations.AddField(
            model_name='article2tag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='responsitory.TagInfo', verbose_name='标签'),
        ),
        migrations.AlterUniqueTogether(
            name='star2fans',
            unique_together=set([('fans_user', 'star_user')]),
        ),
        migrations.AlterUniqueTogether(
            name='categoryinfo',
            unique_together=set([('title', 'blog')]),
        ),
        migrations.AlterUniqueTogether(
            name='article2tag',
            unique_together=set([('article', 'tag')]),
        ),
    ]