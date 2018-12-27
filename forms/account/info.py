from django import forms
from django.forms import fields
from responsitory.models import UserDetail, UserInfo


class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = '__all__'
        # exclude = ['location']

    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class': 'form-control'})  # 传入组件属性
        return super(UserDetailForm, cls).__new__(cls)


class UserImgForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['img']


