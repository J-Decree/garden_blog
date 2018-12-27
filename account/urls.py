from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^geetest/login$', views.geetest_login, name='geetest_login'),
    url(r'^loginOut$', views.logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^register_check_username$', views.register_check_username),
    url(r'^verify_code$', views.create_verify_code),
    url(r'^create_geetest_verify$', views.create_geetest_verify),
    url(r'^userinfo/$', views.user_info, name='user_info'),
    url(r'^get_city/$', views.get_city),
    url(r'^get_town/$', views.get_town),
    url(r'^upload_avatar/$', views.upload_avatar),
]
