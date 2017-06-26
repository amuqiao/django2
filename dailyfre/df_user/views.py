# coding=utf-8
from django.http.response import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from models import *
from hashlib import sha1  # sha1加密
import user_decorator

# Create your views here.


def register(request):
    """
    注册界面
    """
    context = {'title': '用户注册'}
    return render(request, "df_user/register.html", context)


def register_handle(request):
    """
    1.接收用户输入信息
    2.判断用户是否注册,将用户注册信息提交到数据库
    3.注册成功,转到登陆页面
    """
    # 接收form表单POST提交数据
    post = request.POST
    uname = post.get('user_name')
    print uname
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')

    # 判断两次输入的密码是否相同
    if upwd != upwd2:
        return redirect('/user/register/')

    # 密码采用sha1进行加密后,保存到数据库中
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()
    print upwd3

    # 创建UserInfo对象,保存用户信息,并存入数据库中
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    print 1

    # 注册成功,redirect重定向到登陆界面
    return redirect('/user/login/')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    """
    登陆界面
    """
    # 获取cookie中uname的值,若不存在,初始化为空
    uname = request.COOKIES.get('uname', '')
    context = {
        'title': '用户登录',
        'error_name': 0,
        'error_pwd': 0,
        'uname': uname}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    """
    用户登陆处理
    登陆成功,跳转到用户中心
    context信息返回给form表单,用于提示信息(用户名或密码错误)
    """
    # 接收form表单post请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)  # []
    print uname
    # 判断：如果未查到则用户名错，如果查到则判断密码是否正确，正确则转到用户中心
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest() == users[0].upwd:
            # 获取cookie中red_url的值,若没有则置为'/',用于登陆后返回之前浏览的页面
            url = request.COOKIES.get('red_url', '/')
            # red = HttpResponseRedirect(url)
            red = redirect(url)
            # 成功后删除转向地址，防止以后直接登录造成的转向
            red.set_cookie('red_url', '', max_age=-1)
            # 记住用户名 用session保存用户名
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {
                'title': '用户登录',
                'error_name': 0,
                'error_pwd': 1,
                'uname': uname,
                'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {
            'title': '用户登录',
            'error_name': 1,
            'error_pwd': 0,
            'uname': uname,
            'upwd': upwd}
        return render(request, 'df_user/login.html', context)


def logout(request):
    """
    退出登陆
    清除session信息
    """
    request.session.flush()
    return redirect('/')


@user_decorator.login
def info(request):
    """
    显示用户信息
    显示最近浏览商品信息
    """
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    context = {'title': '用户中心',
               'user_email': user_email,
               # 从session中读取用户名
               'user_name': request.session['user_name'],
               'page_name': 1,
               }
    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def order(request):
    """
    显示订单信息
    """
    return render(request, 'df_user/user_center_order.html')


@user_decorator.login
def site(request):
    """
    用户中心:地址页
    用户修改地址信息
    """
    # 从session中读取用户信息,显示用户登陆状态
    user = UserInfo.objects.get(id=request.session['user_id'])
    # 用户修改地址信息提交时触发
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title': '用户中心', 'user': user,
               'page_name': 1}
    return render(request, 'df_user/user_center_site.html', context)
