import hashlib
from functools import wraps
from django.shortcuts import redirect
from django.http import JsonResponse


def md5(password):
    m = hashlib.md5()
    m.update(password.encode('utf8'))  # 只能传入字节
    return m.hexdigest()  # 92a7e713c30abbb0319fa07da2a5c4af


def check_login(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if not request.session.get('user_id', ''):
            if request.is_ajax():
                return JsonResponse({'status': 0, 'msg': '请登录后再进行操作'})
            else:
                return redirect('/account/login?next=%s' % request.path)
        return func(request, *args, **kwargs)

    return inner
