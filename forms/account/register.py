from django import forms
from django.forms import fields
from django.forms import widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from responsitory.models import *
from forms.base import BaseForm
from responsitory.models import UserDetail
from utils.account.libs import md5


class RegiseterForm(BaseForm, forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = '__all__'
        exclude = ['detail', 'password', 'img']

    username = fields.CharField(
        min_length=1,
        max_length=20,
        error_messages={'required': 'server:用户名不能为空',
                        'max_length': 'server:用户名长度最长不能超过20',
                        },
        widget=widgets.TextInput(attrs={'name': 'username', 'placeholder': "请输入用户名", \
                                        'class': 'form-control', 'id': 'username'}),
        label='用户名',
    )

    password1 = fields.CharField(
        min_length=6,
        max_length=20,
        widget=widgets.PasswordInput(attrs={'name': 'password1', 'placeholder': "请输入密码", \
                                            'class': 'form-control', 'id': 'password1'}),
        error_messages={'required': 'server:密码不能为空',
                        'min_length': 'server:密码长度不能少于6',
                        'max_length': 'server:密码长度最长不能超过20',
                        },
        validators=[RegexValidator(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).*$', '密码必须包含大小写字母和数字')],
        label='密码',
    )

    password2 = fields.CharField(
        min_length=6,
        max_length=20,
        widget=widgets.PasswordInput(attrs={'name': 'password2', 'placeholder': "请再次输入密码", \
                                            'class': 'form-control', 'id': 'password2'}),
        error_messages={'required': 'server:密码不能为空',
                        },
        label='确认密码',
    )

    phone = fields.CharField(
        min_length=11,
        max_length=12,
        error_messages={'required': 'server:手机号码不能为空',
                        'min_length': 'server:号码必须为11位或者12位',
                        'max_length': 'server:号码必须为11位或者12位',
                        },
        validators=[RegexValidator(r'^1[0-9]{10,11}$', '手机号码格式错误'), ],
        label='电话号码',
        widget=widgets.TextInput(attrs={'name': 'phone', 'placeholder': "请输入手机号码", \
                                        'class': 'form-control', 'id': 'phone'}),
    )

    email = fields.EmailField(
        error_messages={'required': 'server:邮箱不能为空',
                        'invalid': '邮箱格式错误',
                        },
        label='邮箱',
        widget=widgets.TextInput(attrs={'name': 'email', 'placeholder': "请输入邮箱", \
                                        'class': 'form-control', 'id': 'email'})
    )

    verify = fields.CharField(
        error_messages={'required': '验证码不能为空', },
        label='验证码',
        widget=widgets.TextInput(attrs={'name': 'verify', 'placeholder': "请输入验证码", \
                                        'class': 'form-control', 'id': 'verify'})
    )

    def clean_username(self):
        username = self.request.POST.get('username', '')
        res = UserInfo.objects.filter(username=username).first()
        if res:
            raise ValidationError(message='用户名已经存在了', code='invalid')
        else:
            return self.cleaned_data['username']

    def clean_verify(self):
        user_verify_code = self.request.POST.get('verify', '').upper()
        verify_code = self.request.session.get('verify_code').upper()
        if user_verify_code != verify_code:
            raise ValidationError(message='验证码错误', code='invalid')

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1', '')
        if not p1:
            return
        p2 = self.cleaned_data.get('password2', '')
        if p1 != p2:
            raise ValidationError('两次密码输入不一致')
        return self.cleaned_data['password2']

    def save(self, commit=True):
        from django.db import transaction
        try:
            with transaction.atomic():
                user = super(RegiseterForm, self).save(commit=False)
                password = md5(self.cleaned_data['password2'])
                user.password = password
                detail = UserDetail()
                detail.save()
                user.detail = detail
                if commit:
                    user.save()
        except Exception as e:
            print('保存失败', e)
            user = None
        return user
