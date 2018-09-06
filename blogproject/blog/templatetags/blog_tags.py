from ..models import Article,Category
from django import template
from django.db.models.aggregates import Count
from users.models import User
from django.utils.safestring import mark_safe
import markdown



#为了能够通过 {% get_recent_posts %} 的语法在模板中调用这个函数，
# 必须按照 Django 的规定注册这个函数为模板标签

register = template.Library()


# @register.simple_tag()　　1.9以后版本使用
def get_recent_articles(num=5):
    #获得前5篇文章
    return Article.objects.all().order_by('-created_time')[:num]
# 注册后即可在模板中使用
register.simple_tag(get_recent_articles)

#归档模板标签：按月降序归档
def archives():
    return Article.objects.dates('created_time','month',order='DESC')
register.simple_tag(archives)

# 分类模板标签
def get_categories():
    #annotate统计返回的 Category 记录的集合中每条记录下的文章数
    #它接收一个和 Categoty 相关联的模型参数名,post是通过外键关联的
    return Category.objects.annotate(num_articles = Count('article')).filter(num_articles__gt=0)
register.simple_tag(get_categories)

def author_article():
    return User.objects.annotate(author_articles=Count('article')).filter(author_articles__gt=0)
register.simple_tag(author_article)

def get_reading(num=2):
    return Article.objects.all().order_by('reading')[:num]
register.simple_tag(get_reading)

