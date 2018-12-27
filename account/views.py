import json
from io import BytesIO
from django.http import JsonResponse, Http404
from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from responsitory.models import *
from forms import account
from utils import check_login
import utils


# Create your views here.

def login(request):
    if request.method == 'GET':
        form = account.LoginForm(request=request)
        return render(request, 'account/user-login.html', {'form': form})
    else:
        form = account.LoginForm(request=request, data=request.POST)
        if form.is_valid():
            # 判断是否有免登录选项
            request.session['user_id'] = form.user.id
            if form.cleaned_data.get('auto'):
                request.session.set_expiry(60 * 60 * 24 * 30)

            # 判断是否有next参数
            next_url = request.GET.get('next', '')
            redirect_url = next_url if next_url \
                else reverse('user_info', kwargs={})
            return redirect(redirect_url)
        else:
            # print(dict(form.errors))
            return render(request, 'account/user-login.html', {'form': form})


def geetest_login(request):
    if request.method == 'GET':
        return render(request, 'account/geetest-login.html')
    else:
        # ajax 登录 request.is_ajax()
        form = account.GeetestLoginForm(request=request, data=request.POST)
        if form.is_valid():
            request.session['user_id'] = form.user.id
            if form.cleaned_data.get('auto'):
                request.session.set_expiry(60 * 60 * 24 * 30)

            next_url = request.GET.get('next', '')
            redirect_url = next_url if next_url \
                else reverse('user_info', kwargs={})
            ret = {'status': 1, 'redirect_href': redirect_url}
            return JsonResponse(ret)
        else:
            ret = {'status': 0}
            ret.update(utils.format_errors(form.errors))
            return JsonResponse(ret)


def logout(request):
    request.session.clear()
    return redirect('/')


def register_check_username(request):
    username = request.GET.get('username', '')
    res = UserInfo.objects.filter(username=username)
    if len(res) == 0:
        return JsonResponse({'res': True})
    else:
        return JsonResponse({'res': False})


def create_verify_code(request):
    buffer = BytesIO()
    img, code = utils.verify_code.create_validate_code()
    img.save(buffer, 'PNG')
    request.session['verify_code'] = code
    return HttpResponse(buffer.getvalue())


def create_geetest_verify(request):
    from utils.account import geetest
    return HttpResponse(geetest.get_geetest_verify_code(request))


def register(request):
    if request.method == 'GET':
        form = account.RegiseterForm(request)
        context = {'form': form}
        return render(request, 'account/user-register-f.html', context)

    elif request.method == 'POST':
        form = account.RegiseterForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                redirect_url = reverse('user_info', kwargs={})
                return redirect(redirect_url)
            else:
                return HttpResponse('服务器发生未知错误')
        else:
            context = {'form': form}
            return render(request, 'account/user-register-f.html', context)


@check_login
def user_info(request):
    if not request.login_user.detail.location:
        provinces = Province.objects.all()
        citys = City.objects.filter(province_id=provinces.first().id)
        towns = Town.objects.filter(city_id=citys.first().id)
    else:
        user_town = request.login_user.detail.location
        towns = list(Town.objects.exclude(id=user_town.id).filter(city_id=user_town.city.id))
        print(towns)
        towns.insert(0, user_town)
        user_city = user_town.city
        citys = list(City.objects.exclude(id=user_city.id).filter(province_id=user_city.province.id))
        citys.insert(0, user_city)
        user_province = user_city.province
        provinces = list(Province.objects.exclude(id=user_province.id))
        provinces.insert(0, user_province)
    context = {'provinces': provinces, 'citys': citys, 'towns': towns}

    if request.method == 'GET':
        form = account.UserDetailForm(instance=request.login_user.detail)
        context['form'] = form
        return render(request, 'account/user-info.html', context)
    else:
        form = account.UserDetailForm(instance=request.login_user.detail, data=request.POST)
        if form.is_valid():
            form.save()
            utils.flash(request, 'success', '更新个人信息成功')
            return redirect(request.path)
        else:
            context['form'] = form
            return render(request, 'account/user-info.html', context)


@check_login
def upload_avatar(request):
    form = account.UserImgForm(instance=request.login_user, files=request.FILES)
    if form.is_valid():
        form.save()
        ret = {'status': 1}
        return JsonResponse(ret)
    else:
        ret = {'status': 0}
        ret.update(utils.format_errors(form.errors))
        return JsonResponse(ret)


def get_city(request):
    province_id = request.GET.get('province_id')
    citys = City.objects.filter(province_id=province_id).values()
    citys = json.dumps(list(citys))
    return JsonResponse(citys, safe=False)


def get_town(request):
    city_id = request.GET.get('city_id')
    towns = Town.objects.filter(city_id=city_id).values()
    towns = json.dumps(list(towns))
    return JsonResponse(towns, safe=False)
