from django import template

register = template.Library()


@register.filter
def filter_phone(phone_num):
    filter_num = len(phone_num) - 4
    return '*' * filter_num + phone_num[filter_num:]
