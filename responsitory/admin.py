from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserInfo)
# admin.site.register(BillInfo)
admin.site.register(BlogInfo)
admin.site.register(Star2Fans)
admin.site.register(CategoryInfo)
admin.site.register(TagInfo)
# admin.site.register(ArticleInfo)
# admin.site.register(Article2Tag)
admin.site.register(EvaluateInfo)
admin.site.register(CSSInfo)


# admin.site.register(CommentInfo)


class BillAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/static/plugin/kindeditor/kindeditor-all-min.js',
            '/static/plugin/kindeditor/lang/zh_CN.js',
            '/static/plugin/kindeditor/config.js',
        )


admin.site.register(BillInfo, admin_class=BillAdmin)


class ArticleAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/static/plugin/kindeditor/kindeditor-all-min.js',
            '/static/plugin/kindeditor/lang/zh_CN.js',
            '/static/plugin/kindeditor/config.js',
        )


admin.site.register(ArticleInfo, admin_class=ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/static/plugin/kindeditor/kindeditor-all-min.js',
            '/static/plugin/kindeditor/lang/zh_CN.js',
            '/static/plugin/kindeditor/config.js',
        )


admin.site.register(CommentInfo, admin_class=CommentAdmin)
