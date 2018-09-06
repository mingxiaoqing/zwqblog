from django.shortcuts import render,redirect,reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import View
from urllib import parse
from urllib import request as req
import re
import json
import random
from users.models import User,OAuthQQ

#主页
def index(request):
    try:
        openid = request.session.get('openid')
        user=User.objects.first()
        qq_user = user.oauthqq_set.get(qq_openid=openid)
        return render(request,'index.html',{'user':qq_user})
    except:
        return render(request, 'index.html')


class LoginView(View):
    '''登录'''
    def get(self,request):
        '''显示'''
        #如果用户是登录状态,跳转到首页
        if request.user.is_authenticated:
            return redirect('/')
        #session获取来源页面，没有则记录为首页
        # request.session['login_from'] = request.META.get('HTTP_REFERER','/')

        username = request.COOKIES.get('username')
        checked = 'checked'
        if username is None:
            username=''
            checked=''
        return render(request, "users/login.html",{'username':username,'checked':checked})

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember',None)
        if not all([username, password]):
            return render(request, 'users/login.html', {'error': '数据不能为空！'})
        # 验证用户名和密码是否正确，正确则返回user 否则为None
        user = auth.authenticate(username=username, password=password)
        if user:
            # 将登录的用户封装到request.user
            login(request, user)
            # 获取登录之前访问的url，默认为首页
            next_url = request.GET.get('next',reverse('index'))
            # 跳转到next_url
            response = redirect(next_url)
            #判断是否需要记住用户名
            if remember == 'on':
                #设置cookie
                response.set_cookie('username',username,max_age=7*24*3600)
            else:
                #删除cookie
                response.delete_cookie('username')
            return response
            # request.session['username'] = username
            # return HttpResponseRedirect(request.session['login_from'])
        return render(request, "users/login.html", {"error": "用户名或密码不正确！"})


class RegisterView(View):
    '''注册'''
    def get(self,request):
        #获取页面
        return render(request,'users/register.html')

    def post(self,request):
        #提交数据
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if not all([username,email,password,confirm]):
            return render(request,'users/register.html',{'error':'数据不能为空'})

        if User.objects.filter(username=username):
            return render(request, "users/register.html", {'error': '该用户已存在！'})

        if User.objects.filter(email = email):
            return render(request, "users/register.html", {'error':'该邮箱已存在！'})

        if len(password)<6:
            return render(request, "users/register.html", {'error':'密码长度不能小于6位！'})

        if password != confirm:
            return render(request, "users/register.html", {'error': '两次输入密码不一致！'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return HttpResponseRedirect(reverse('user:login'))


class LogoutView(View):
    '''登出'''
    def get(self,request):
        # 清除用户登录状态　系统logout会自动清除session
        logout(request)
        return HttpResponseRedirect(reverse('user:login'))
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


#编辑个人信息
@login_required
def editUserInfo(request):
    if request.method=='GET':
        user = User.objects.get(username=request.user.username)
        return render(request,'users/info.html',{'user':user})
    elif request.method =='POST':
        try:
            image = request.FILES.get('img')
            name = request.POST.get('name')
            nick_name = request.POST.get('nick_name')
            birday = request.POST.get('birday')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            mobile = request.POST.get('mobile')
            sign = request.POST.get('sign')
        except:
            msg = '数据填写有误，请重新填写'
            return render(request, 'users/info.html',{'msg':msg})
        user = User.objects.get(username = request.user)
        if image:
            user.image=image
        user.name = name
        user.birday=birday
        user.nick_name=nick_name
        user.gender=gender
        user.address=address
        user.mobile=mobile
        user.sign=sign
        user.save()
        return HttpResponseRedirect(reverse('user:editinfo'))



