from django.utils.deprecation import MiddlewareMixin
from responsitory.models import UserInfo


class AuthMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id', '')
        if user_id:
            user = UserInfo.objects.filter(id=user_id).first()
            request.login_user = user
        else:
            request.login_user = None
