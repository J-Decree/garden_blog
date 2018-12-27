from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<surfix>\w+)/$', views.blog, name='blog'),
    url(r'^(?P<surfix>\w+)/(?P<condition>((tag)|(category)|(date)))=(?P<value>.+)/$', views.blog,
        name='blog_condition'),
    url(r'^(?P<surfix>\w+)/(?P<article_id>\d+)/$', views.blog_article, name='blog_article'),
    url(r'^(?P<surfix>\w+)/(?P<article_id>\d+)/action/', views.action, name='action'),
    url(r'(?P<surfix>\w+)/(?P<article_id>\d+)/get_comments/', views.get_comments, name='get_comments'),
    url(r'(?P<surfix>\w+)/(?P<article_id>\d+)/add_comment/', views.add_comment, name='add_comment'),
    url(r'(?P<surfix>\w+)/(?P<article_id>\d+)/upload/kindeditor/', views.kindeditor_upload, name='kindeditor_upload'),
    url(r'^type_(?P<index_kind>[1-3])', views.index, name='index_conditon'),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<surfix>\w+)/(?P<article_id>\d+)/page_handler$', views.page_handler),
]
