from django.db import models


def upload_to(instance, filename):
    import uuid
    filename = '%s-%s' % (str(uuid.uuid4())[:8], filename)
    return '/'.join(['head', instance.username, filename])


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=16, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=64, verbose_name='密码')
    email = models.EmailField(max_length=32, verbose_name='邮箱', unique=True)
    phone = models.CharField(max_length=11, verbose_name='手机号码', unique=True)
    img = models.ImageField(verbose_name='用户头像', default='head/default.jpg', upload_to=upload_to)
    enroll_date = models.DateField(auto_now_add=True, verbose_name='创建时间')
    detail = models.OneToOneField('UserDetail', verbose_name='用户详细信息')

    class Meta:
        db_table = 'UserInfo'
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.username


class UserDetail(models.Model):
    signature = models.CharField(max_length=128, null=True, blank=True, verbose_name='个性签名')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    location = models.ForeignKey('Town', verbose_name='所在地', blank=True, null=True)
    location_detail = models.CharField(max_length=128, verbose_name='详细住址', blank=True, null=True)
    interest = models.ManyToManyField('StudyPoint', blank=True, null=True, verbose_name='兴趣技术点')


class StudyPoint(models.Model):
    title = models.CharField(max_length=32, verbose_name='技术名字')

    def __str__(self):
        return self.title


class Province(models.Model):
    title = models.CharField(max_length=12, verbose_name='省份名')


class City(models.Model):
    title = models.CharField(max_length=12, verbose_name='市名')
    province = models.ForeignKey('Province', verbose_name='所属省份')


class Town(models.Model):
    title = models.CharField(max_length=12, verbose_name='镇名')
    city = models.ForeignKey('City', verbose_name='所属市')

    def __str__(self):
        return self.title


class ArticleManager(models.Manager):
    def distinct_date(self, **kwargs):
        l = self.filter(**kwargs).values('time')
        res = set()
        for obj in l:
            # obj['time']是datetime.datetime对象
            t = obj['time'].strftime('%Y-%m')
            res.add(t)
        return res


class ArticleInfo(models.Model):
    blog = models.ForeignKey('BlogInfo', on_delete=models.CASCADE, verbose_name='所属博客')
    title = models.CharField(max_length=50, verbose_name='文章标题')
    summary = models.TextField(verbose_name='简介', null=True)
    time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    detail = models.TextField(verbose_name='文章内容')
    index_type = models.IntegerField(choices=[(1, '技术'), (2, '新闻'), (3, '其他')], verbose_name='总分类', default=1,
                                     help_text='固定分类')
    read_num = models.IntegerField(default=0, verbose_name='阅读量')
    category = models.ForeignKey('CategoryInfo', verbose_name='种类', null=True, blank=True, help_text='用户自定义分类')
    tags = models.ManyToManyField('TagInfo', verbose_name='标签', null=True, blank=True)

    objects = ArticleManager()  # 自定义管理器

    class Meta:
        db_table = 'ArticleInfo'
        verbose_name_plural = '文章表'

    def __str__(self):
        return self.title


class CSSInfo(models.Model):
    title = models.CharField(max_length=16, verbose_name='主题名')
    file = models.FileField(verbose_name='css文件', upload_to='css')

    def __str__(self):
        return self.title


class BlogInfo(models.Model):
    surfix = models.CharField(max_length=16, verbose_name='url后缀', unique=True)
    signature = models.CharField(max_length=30, verbose_name='个性签名')
    title = models.CharField(max_length=16, verbose_name='标题')
    user = models.ForeignKey('UserInfo', verbose_name='所属用户')
    css = models.OneToOneField('CSSInfo', verbose_name='主题样式', default=1)

    class Meta:
        db_table = 'BlogInfo'
        verbose_name_plural = '个人博客表'

    def __str__(self):
        return self.title


class TagInfo(models.Model):
    title = models.CharField(max_length=8, verbose_name='博客标题')
    blog = models.ForeignKey('BlogInfo', verbose_name='所属博客')

    class Meta:
        db_table = 'TagInfo'
        verbose_name_plural = '标签表'

    def __str__(self):
        return self.title


#
# class Article2Tag(models.Model):
#     article = models.ForeignKey('ArticleInfo', verbose_name='所属文章')
#     tag = models.ForeignKey('TagInfo', verbose_name='标签')
#
#     class Meta:
#         db_table = 'Article2Tag'
#         unique_together = ['article', 'tag']
#
#     def __str__(self):
#         return '%s 2 %s' % (self.article.title, self.tag.title)


class CommentInfo(models.Model):
    time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    detail = models.TextField(verbose_name='评论详细')
    article = models.ForeignKey('ArticleInfo', verbose_name='所属文章', null=True, blank=True)
    comment_parent = models.ForeignKey('self', blank=True, null=True, verbose_name='父评论')
    user = models.ForeignKey('UserInfo', verbose_name='所属用户')

    class Meta:
        db_table = 'CommentInfo'
        verbose_name_plural = '评论表'

    def __str__(self):
        return '%s对《%s》的评论 ' % (self.user.username, self.article.title)


class BillInfo(models.Model):
    uuid = models.CharField(max_length=32, verbose_name='唯一标志')
    title = models.CharField(max_length=128, verbose_name='标题')
    detail = models.TextField(verbose_name='详细')
    submit_time = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')
    status = models.IntegerField(choices=[(1, '未处理'), (2, '待处理'), (3, '已处理')], verbose_name='状态')
    handler = models.ForeignKey('UserInfo', verbose_name='处理者', blank=True, null=True, related_name='handler_bill')
    submitter = models.ForeignKey('UserInfo', verbose_name='提交者', related_name='submitter_bill')
    solution = models.TextField(verbose_name='解决办法', null=True, blank=True)
    evaluate = models.TextField(verbose_name='评价信息', null=True, blank=True)
    handle_time = models.DateTimeField(verbose_name='处理时间', null=True, blank=True)

    class Meta:
        db_table = 'BillInfo'
        verbose_name_plural = '保障信息表'

    def __str__(self):
        return self.title


class EvaluateInfo(models.Model):
    action = models.IntegerField(choices=[(1, '赞'), (-1, '踩')], verbose_name='动作')
    article = models.ForeignKey('ArticleInfo', verbose_name='所属文章')
    user = models.ForeignKey('UserInfo', verbose_name='动作所属用户')

    class Meta:
        db_table = 'EvaluateInfo'
        verbose_name_plural = '踩赞表'
        unique_together = ['article', 'user']

    def __str__(self):
        return '%s %s 《%s》' % (self.user.username, self.get_action_display(), self.article.title)


class Star2Fans(models.Model):
    fans_user = models.ForeignKey('UserInfo', verbose_name='粉丝', related_name='fans')
    star_user = models.ForeignKey('UserInfo', verbose_name='被粉者', related_name='stars')

    class Meta:
        unique_together = ['fans_user', 'star_user']
        db_table = 'Star2Fans'

    def __str__(self):
        return '%s 粉 %s' % (self.fans_user.username, self.star_user.username)


class CategoryInfo(models.Model):
    title = models.CharField(max_length=16, verbose_name='种类名')
    blog = models.ForeignKey('BlogInfo', verbose_name='所属博客')

    class Meta:
        unique_together = ['title', 'blog']
        db_table = 'CategoryInfo'
        verbose_name_plural = '种类表'

    def __str__(self):
        return self.title
