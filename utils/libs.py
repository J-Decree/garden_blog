import uuid


def get_uuid():
    return str(uuid.uuid4())


def format_errors(errors):
    """
    {'username': ['用户名不存在'], 'verify': ['验证码错误']}
    :return: {'username': '用户名不存在', 'verify': '验证码错误'}
    """
    errors = dict(errors)
    return {k: v[0] for k, v in errors.items()}


def format_first_errors(errors):
    """
       {'username': ['用户名不存在'], 'verify': ['验证码错误']}
       :return: {'msg': '用户名不存在'}
    """
    errors = dict(errors)
    for k, v in errors.items():
        return {'msg': '%s:%s' % (k, v[0])}
