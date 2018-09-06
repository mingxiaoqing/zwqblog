from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        #表明表单对应的数据库模型是Comment类
        model = Comment
        #指定表单需要显示的字段
        fields = ['text']
