import xadmin
from xadmin import views
from .models import Category,Article

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = '博客后台管理系统'
    site_footer = '我的博客'
    #可收缩列
    # menu_style = 'accordion'

class CategoryAdmin(object):
    list_display = ['name']
    search_field = ['name']
    list_filter = ['name']

class ArticleAdmin(object):
    list_display = ['author','title','category','created_time','modified_time','reading']
    search_field = ['author','title','category','created_time']
    list_filter = ['author','title','created_time']
    ordering = ['-reading']


xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.register(Category,CategoryAdmin)
xadmin.site.register(Article,ArticleAdmin)