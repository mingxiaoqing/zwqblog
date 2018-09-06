from django.conf.urls import url
from . import views

app_name = 'comments'
urlpatterns = [
    url(r'^article/(?P<article_pk>[0-9]+$)',views.article_comment,name='article_comment'),
    url(r'^contact_msg',views.contact,name='contact_msg')
]