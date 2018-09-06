from django.forms import ModelForm
from .models import Article


class MDEditorForm(ModelForm):
    '''文章发布'''
    class Meta:
        model = Article
        fields=['title','body','category']
