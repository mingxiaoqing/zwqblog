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


def to_login(request):
    state = random.randrange(100000, 999999) # 定义一个随机状态码，防止跨域伪造攻击。
    request.session['state'] = state  # 将随机状态码存入Session，用于授权信息返回时验证。
    client_id = '***'  # QQ互联中网站应用的APP ID。
    callback = parse.urlencode({'redirect_uri': 'http://www.reliapp.cn/qqlogin'})
    # 对回调地址进行编码，用户同意授权后将调用此链接。
    login_url = 'https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=%s&%s&state=%s' % (
        client_id, callback, state)  # 组织QQ第三方登录链接
    return HttpResponseRedirect(login_url)  # 重定向到QQ第三方登录授权页面


def qqlogin(request):

    if request.GET['state']== request.session['state']:  # 验证状态码，防止跨域伪造攻击。
        code = request.GET['code'] # 获取用户授权码
        client_id = '**'  # QQ互联中网站应用的APP ID。
        client_secret = '＊＊'  # QQ互联中网站应用的APP Key。
        callback = parse.urlencode({'redirect_uri': 'http://www.reliapp.cn/qqlogin'})
        # 对回调地址进行编码，用户同意授权后将调用此链接。
        login_url = 'https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&code=%s&client_id=%s&client_secret=%s&%s' % (
            code, client_id, client_secret, callback)  # 组织获取访问令牌的链接
        response = req.urlopen(login_url).read().decode()  # 打开获取访问令牌的链接
        access_token = re.split('&', response)[0]  # 获取访问令牌
        res = req.urlopen('https://graph.qq.com/oauth2.0/me?' + access_token).read().decode()

        openid = json.loads(parse_jsonp(res))['openid']  # 从返回数据中获取openid
        userinfo = req.urlopen('https://graph.qq.com/user/get_user_info?oauth_consumer_key=%s&openid=%s&%s' % (
            client_id, openid, access_token)).read().decode()  # 打开获取用户信息的链接
        userinfo = json.loads(userinfo)  # 将返回的用户信息数据（JSON格式）读取为字典。
        try:
            qq_user = OAuthQQ.objects.get(qq_openid=openid)
        except:
            qq_user = OAuthQQ()
            qq_user.qq_openid=openid
            qq_user.save()
        else:
            user = qq_user.user
            user.nick_name = userinfo['nickname']
            user.gender = userinfo['gender']
            user.image=userinfo['figureurl_qq_1']
            user.save()
            login(request,user)
        request.session['openid'] = openid  # 将已登录的用户openid写入Session
        return render(request, 'index.html')

    else:
        return render(request, 'users/login.html',{'error':'QQ授权失败，请用用户名登录'})

#为了获取返回数据中的openid的解析函数
def parse_jsonp(jsonp_str):
    try:
        return re.search('^[^(]*?\((.*)\)[^)]*$', jsonp_str).group(1)
    except:
        raise ValueError('无效数据！')
