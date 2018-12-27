# from django.test import TestCase

import os

from django.core import serializers

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ErrorReport.settings")
    import django

    django.setup()
    from responsitory.models import *
    from responsitory.Models.web import *

    a = CommentInfo.objects.first()
    print(a)
    m = CommentInfoModel.from_comment_obj(a)
    print(m.serialize())