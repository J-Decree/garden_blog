import os
from django.db.models.fields.files import FileField, ImageFieldFile
from django.conf import settings
from responsitory.models import *
from django.db import models


class BaseModel(object):
    def serialize(self):
        from datetime import datetime, date
        ret = {}
        for k, v in self.__dict__.items():
            if hasattr(v, 'serialize'):
                ret[k] = v.serialize()
            elif isinstance(v, datetime):
                ret[k] = v.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(v, date):
                ret[k] = v.strftime('%Y-%m-%d')
            elif isinstance(v, ImageFieldFile) or isinstance(v, FileField):
                ret[k] = os.path.join(settings.MEDIA_URL, str(v))
            else:
                ret[k] = v
        return ret


class UserInfoModel(BaseModel):
    def __init__(self, id, username, email, phone, img, enroll_date):
        self.id = id
        self.username = username
        self.email = email
        self.phone = phone
        self.img = img
        self.enroll_date = enroll_date

    @classmethod
    def from_user_obj(cls, user_obj: UserInfo):
        return cls(user_obj.id, user_obj.username, user_obj.email, user_obj.phone, user_obj.img, user_obj.enroll_date)


class ArticleInfoModel(BaseModel):
    def __init__(self, title):
        self.title = title

    @classmethod
    def from_article_obj(cls, article_obj):
        return cls(article_obj.title)


class CommentParentModel(BaseModel):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @classmethod
    def from_parent_comment_obj(cls, parent_comment_obj):
        if not parent_comment_obj:
            return None
        return cls(
            id=parent_comment_obj.id,
            username=parent_comment_obj.user.username
        )


class CommentInfoModel(BaseModel):
    def __init__(self, id, time, detail, comment_parent_obj, user_obj):
        self.id = id
        self.time = time
        self.detail = detail
        self.comment_parent_obj = comment_parent_obj
        self.user_obj = user_obj

    @classmethod
    def from_comment_obj(cls, comment_obj: CommentInfo):
        if not comment_obj:
            return None
        return cls(
            comment_obj.id,
            comment_obj.time,
            comment_obj.detail,
            CommentParentModel.from_parent_comment_obj(comment_obj.comment_parent),
            UserInfoModel.from_user_obj(comment_obj.user),
        )


class CommentCollectionModel(BaseModel):
    def __init__(self, comment_objs):
        self.comment_objs = None
        self.__init_collection(comment_objs=comment_objs)

    def __init_collection(self, comment_objs):
        self.comment_objs = [CommentInfoModel.from_comment_obj(obj) for obj in comment_objs]

    def serialize(self):
        return [model_obj.serialize() for model_obj in self.comment_objs]
