import xadmin
from .models import Comment,Contact

class CommentAdmin(object):
    list_display = ['name','text','created_time','article']
    search_field = ['name','text','created_time','article']
    list_filter = ['name','text','created_time','article']

class ContactAdmin(object):
    list_display = ['name','email','subject','message']
    search_field = ['name','email','subject','message']
    list_filter = ['name','email','subject','message']

xadmin.site.register(Comment,CommentAdmin)
xadmin.site.register(Contact,ContactAdmin)