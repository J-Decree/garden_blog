from django import forms
from django.forms import fields
from django.forms import widgets
from django.core.exceptions import ValidationError
from responsitory.models import *
from forms.base import BaseForm
from utils.account.libs import md5


class LoginForm(BaseForm, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    username = fields.CharField(
        error_messages={'required': '用户名不能为空',
                        },
        widget=widgets.TextInput(attrs={'name': 'username', 'placeholder': "请输入用户名", \
                                        'class': 'form-control', 'id': 'username'}),
        label='用户名',
    )

    password = fields.CharField(
        error_messages={'required': '密码不能为空'},
        widget=widgets.PasswordInput(attrs={'name': 'password', 'placeholder': "请输入密码", \
                                            'class': 'form-control', 'id': 'password'}),
        label='密码',
    )

    verify = fields.CharField(
        error_messages={'required': '验证码不能为空'},
        widget=widgets.TextInput(attrs={'name': 'verify', 'placeholder': "请输入验证码", \
                                        'class': 'form-control', 'id': 'verify'}),
        label='验证码',
    )

    auto = forms.CharField(
        label='一个月内自动登录',
        widget=widgets.CheckboxInput(attrs={'id': "auto", 'name': 'auto'}),
        required=False,
    )

    #
    # def clean(self):
    #     username = self.cleaned_data.get('username', '')
    #     password = self.cleaned_data.get('password', '')
    #     try:
    #         UserInfo.objects.get(username=username, password=password)
    #     except UserInfo.DoesNotExist:
    #         raise ValidationError('用户名不存在或密码错误')

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        try:
            user = UserInfo.objects.get(username=username)
            self.user = user
        except UserInfo.DoesNotExist:
            raise ValidationError('用户名不存在')
        else:
            return self.cleaned_data['username']

    def clean_password(self):
        if not self.user:
            return
        password = self.cleaned_data.get('password')
        if self.user.password != md5(password):
            raise ValidationError('密码错误')

        return self.cleaned_data['password']

    def clean_verify(self):
        user_verify_code = self.request.POST.get('verify', '').upper()
        verify_code = self.request.session.get('verify_code').upper()
        if user_verify_code != verify_code:
            raise ValidationError(message='验证码错误', code='invalid')


class GeetestLoginForm(BaseForm, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    username = fields.CharField(
        error_messages={'required': '用户名不能为空',
                        },
    )

    password = fields.CharField(
        error_messages={'required': '密码不能为空'},
    )

    auto = forms.CharField(
        required=False,
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        try:
            user = UserInfo.objects.get(username=username)
            self.user = user
        except UserInfo.DoesNotExist:
            raise ValidationError('用户名不存在')
        else:
            return self.cleaned_data['username']

    def clean_password(self):
        if not self.user:
            return
        password = self.cleaned_data.get('password')
        if self.user.password != md5(password):
            raise ValidationError('密码错误')

        return self.cleaned_data['password']

    def clean(self):
        from utils.account import geetest
        result = geetest.geetest_validate(request=self.request)
        if not result:
            raise ValidationError('验证码错误')
