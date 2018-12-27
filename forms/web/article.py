from bs4 import BeautifulSoup
from django import forms
from django.forms import fields
from django.core.exceptions import ValidationError
from django.conf import settings
from responsitory.models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentInfo
        fields = "__all__"

    def clean_detail(self):
        print('XXXXXXXXXX')
        detail = self.cleaned_data['detail']
        bs = BeautifulSoup(detail, 'html.parser')
        text = bs.text
        if len(text) > 255:
            raise ValidationError('评论内容太长,请限制在255字以内')

        for tag in bs.find_all():
            if tag in settings.FILTER_LIST:
                print('ddddddd', tag)
                tag.decompose()
        return str(bs)
