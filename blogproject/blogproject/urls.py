"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url,include
from django.contrib import admin
from users import views
from . import settings
from django.conf.urls.static import static
import xadmin

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^myblog/', xadmin.site.urls),
    url(r'^blog/',include('blog.urls',namespace='blog')),
    url(r'user/',include('users.urls',namespace='user')),
    url('^comments/',include('comments.urls',namespace='comments')),
    url(r'^users/', include('django.contrib.auth.urls')),
    url(r'mdeditor/', include('mdeditor.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^qqlogin/',views.qqlogin,name='qqlogin')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

