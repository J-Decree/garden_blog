import os
import json
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.conf import settings
from responsitory.models import *
from responsitory.Models.web import *
from utils import check_login
import utils


def index(request, **kwargs):
    return render(request, 'web/index.html')


def blog(request, **kwargs):
    surfix = kwargs['surfix']
    blog = get_object_or_404(BlogInfo, surfix=surfix)
    condition = kwargs.get('condition', '')
    p = request.GET.get('p')
    query_set = None

    if condition == '':
        # 没带条件，获取全部文章
        query_set = ArticleInfo.objects.filter(blog=blog).order_by('-time')
    # url带有条件
    elif condition == 'tag':
        query_set = ArticleInfo.objects.filter(blog=blog, tags__id=int(kwargs['value'])).order_by('-time')
    elif condition == 'category':
        query_set = ArticleInfo.objects.filter(blog=blog, category_id=int(kwargs['value'])).order_by('-time')
    elif condition == 'date':
        query_set = ArticleInfo.objects.filter(blog=blog). \
            extra(where=['date_format(time,"%%Y-%%m")=%s'], params=[kwargs['value'], ]).order_by('-time')

    page_helper = utils.PageHelper(query_set, request, p)
    context = {
        'title': '%s' % blog.title,
        'blog': blog,
        'page_helper': page_helper
    }
    return render(request, 'web/blog.html', context)


def blog_article(request, surfix, article_id):
    blog = get_object_or_404(BlogInfo, surfix=surfix)
    article = get_object_or_404(ArticleInfo, blog=blog, id=article_id)

    context = {
        'title': '%s' % article.title,
        'blog': blog,
        'article': article,
    }
    rep = render(request, 'web/blog-article.html', context)
    reader = utils.ArticleReaderHandler(request, rep)
    if not reader.check_article_been_read(article_id):
        article.read_num += 1
        article.save()
    return rep


@check_login
def action(request, surfix, article_id):
    """
    文章的赞或踩
    """
    from django.db.utils import IntegrityError
    user = request.login_user
    try:
        action = int(request.GET['action'])
        exist_obj = EvaluateInfo.objects.filter(user=user, article_id=article_id, action=action).first()
        if exist_obj:
            exist_obj.delete()
        else:
            EvaluateInfo.objects.create(user=user, action=action, article_id=article_id)
    except IntegrityError:
        return JsonResponse({'status': 0, 'msg': '不允许重复操作'})
    except Exception:
        return JsonResponse({'status': 0, 'msg': '发生未知错误'})

    ret = {'status': 1, 'msg': 'success'}
    query_set = ArticleInfo.objects.filter(id=article_id, evaluateinfo__action=action) \
        .annotate(count=Count('evaluateinfo')).values('count')
    action_count = utils.get_article_action_count(query_set)
    ret['data'] = {'action_count': action_count}
    return JsonResponse(ret)


def get_comments(request, surfix, article_id):
    try:
        root_comments = CommentInfo.objects.filter(article_id=article_id, comment_parent__isnull=True).order_by('time')
        leaf_comments = CommentInfo.objects.filter(article_id=article_id, comment_parent__isnull=False).order_by('time')
        query_set = list(root_comments) + list(leaf_comments)
        data = CommentCollectionModel(query_set).serialize()
        return JsonResponse({'status': 1, 'data': data})
    except Exception as  e:
        print(e)
        return JsonResponse({'status': 0, 'msg': '请求错误'})


@check_login
def add_comment(request, surfix, article_id):
    from forms.web.article import CommentForm
    data = {
        'detail': request.POST.get('detail'),
        'comment_parent': request.POST.get('comment_parent_id', None),  # modelform即使是外键，默认都是原字段名
        'article': article_id,
        'user': request.login_user.id
    }
    form = CommentForm(data=data)
    if form.is_valid():
        obj = form.save()
        ser_obj = CommentInfoModel.from_comment_obj(obj).serialize()
        ret = {'status': 1, 'msg': 'success', 'data': ser_obj}
        return JsonResponse(ret)
    else:
        ret = {'status': 0, }
        ret.update(utils.format_first_errors(form.errors))
        return JsonResponse(ret)


@check_login
def kindeditor_upload(request, surfix, article_id):
    print(dir(request.FILES))
    username = request.login_user.username
    upload_path = os.path.join(settings.MEDIA_ROOT, 'kindeditor', username)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    try:
        file_name = utils.get_uuid()
        file_path = os.path.join(upload_path, file_name)
        file_obj = request.FILES['upload_img']
        with open(file_path, 'wb') as f:
            for line in file_obj:
                f.write(line)

        file_url = os.path.join(settings.MEDIA_URL, 'kindeditor', username, file_name)
        ret = {
            "error": 0,
            "url": file_url
        }
    except Exception as e:
        ret = {
            "error": 1,
            "message": str(e)
        }

    return JsonResponse(ret)


def page_handler(request, surfix, article_id):
    p = request.GET.get('p')
    try:
        article = ArticleInfo.objects.get(id=article_id)
    except ArticleInfo.DoesNotExist:
        return JsonResponse({'error': '文章不存在'})

    comment_count = CommentInfo.objects.filter(article=article).count()
    page = utils.pagination.Pagination(p, comment_count, per_page_count=5)
    comment_list = CommentInfo.objects.filter(article=article). \
                       select_related('comment_parent').order_by('time')[page.start:page.end]
    comment_list = list(comment_list)
    res = []
    for obj in comment_list:
        if obj.comment_parent:
            comment_parent_username = obj.comment_parent.user.username
        else:
            comment_parent_username = None
        tmp = {
            'id': obj.id,
            'time': obj.time.strftime('%Y年-%m月-%d日 %H:%M'),
            'username': obj.user.username,
            'detail': obj.detail,
            'comment_parent_username': comment_parent_username,
        }
        res.append(tmp)

    return JsonResponse(res, safe=False)
