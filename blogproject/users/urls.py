from django.conf.urls import url
from . import views

#告诉 Django 这个 urls.py 模块是属于 users 应用的，这种技术叫做视图函数命名空间。
app_name = 'users'
#参数 name将作为处理函数 index 的别名
urlpatterns=[
    url(r'^login/$',views.LoginView.as_view(),name='login'),
    url(r'^register/$',views.RegisterView.as_view(),name='register'),
    url(r'^logout/$',views.LogoutView.as_view(),name='logout'),
    #编辑个人信息
    url(r'^editinfo/$', views.editUserInfo, name='editinfo'),
    url(r'to_login/',views.to_login,name='to_login'),

]