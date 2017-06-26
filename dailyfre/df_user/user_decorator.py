# coding=utf-8
from django.shortcuts import redirect
from django.http import JsonResponse


def login(func):
    """
    装饰器:若用户未登陆则跳转到登陆页
    """
    def login_fun(request, *args, **kwargs):
        if 'user_id' in request.session:
            return func(request, *args, **kwargs)
        else:
            # 商品详细页 添加至购物车是ajax请求
            if request.is_ajax():
                return JsonResponse({'islogin': 0})
            else:
                return redirect('/user/login/')
                # red.set_cookie('url',request.get_full_path())
                # return red

    return login_fun


'''
http://127.0.0.1:8080/200/?type=10
request.path：表示当前路径，为/200/
request.get_full_path()：表示完整路径，为/200/?type=10
'''
