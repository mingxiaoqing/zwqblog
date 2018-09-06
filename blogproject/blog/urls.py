from django.conf.urls import url
from . import views

#告诉 Django 这个 urls.py 模块是属于 blog 应用的，这种技术叫做视图函数命名空间。
app_name = 'blog'
#参数 name将作为处理函数 index 的别名
urlpatterns=[
    #以 artical/ 开头，后跟一个至少一位数的数字，并且以 / 符号结尾
    #实际上视图函数的调用就是这个样子：detail(request, pk=255)
    url(r'^Article/(?P<pk>[0-9]+)/$', views.ArticleDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesView.as_view(),name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$',views.CategoryView.as_view(),name='category'),
    #文章列表
    url(r'^list/',views.BlogShowView.as_view(),name='list'),
    # 增加分类
    url(r'^addCategory/', views.add_category, name='addCategory'),
    #发表文章
    url(r'^publish/',views.Article_publish,name='publish'),
    #用户文章页
    url(r'^authorArticle/(?P<pk>[0-9]+)/$', views.User_article.as_view(), name='authorArticle'),
    #删除文章
    url(r'^delArticle/(?P<pk>[0-9]+)/$', views.Delete_article, name='delArticle'),
    #编辑文章
    url(r'^editArticle/(?P<pk>[0-9]+)/$', views.Edit_article, name='editArticle'),
]