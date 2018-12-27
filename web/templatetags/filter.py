from django import template
from django.db.models import Count

from responsitory.models import *

register = template.Library()


@register.filter
def up_count(article):
    return EvaluateInfo.objects.filter(action=1, article=article).count()


@register.filter
def down_count(article):
    return EvaluateInfo.objects.filter(action=-1, article=article).count()


@register.inclusion_tag('web/sub/common_bar.html')
def get_common_bar(blog):
    tag_statistics = TagInfo.objects.filter(blog=blog). \
        annotate(article_count=Count('articleinfo')).values('id', 'article_count', 'title')

    category_statistics = CategoryInfo.objects.filter(blog=blog). \
        annotate(article_count=Count('articleinfo')).values('id', 'article_count', 'title')

    date_statistics = ArticleInfo.objects.filter(blog_id=1). \
        extra(select={'create_date': 'date_format(time,"%%Y-%%m")'}). \
        values('create_date').annotate(article_count=Count('id')).values('article_count', 'create_date')

    # 粉丝数
    fans_count = Star2Fans.objects.filter(star_user=blog.user).count()
    # 关注数
    star_count = Star2Fans.objects.filter(fans_user=blog.user).count()

    # 模版只会根据这个函数返回的上下文进行渲染
    return locals()
