from django.db import models
#处理注册登录等流程内置模型中导入User  用户模型
# from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from mdeditor.fields import MDTextField
from django.utils.html import strip_tags


#分类模型
class Category(models.Model):
    name = models.CharField(max_length=30)
    class Meta:
        verbose_name_plural = u'分类列表'
    def __str__(self):
        return self.name

#文章模型
class Article(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')
    body = MDTextField(verbose_name='文章内容')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='发表时间')
    modified_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    #文章摘要可以为空，下文函数将设置为默认摘取文章前**字符显示
    excerpt = models.CharField(max_length=200,blank = True,verbose_name='文章摘要')
    category = models.ForeignKey(Category,verbose_name='分类')
    author = models.ForeignKey('users.User',verbose_name='作者')
    #阅读量为正整数
    reading = models.PositiveIntegerField(verbose_name='阅读量',default=0)
    def __str__(self):
        return self.title

    #自定义 get_absolute_url 方法
    def get_absolute_url(self):
        #第一个参数blog 应用下的 name=detail 的函数
        #如果 Article 的 id（或者 pk，这里 pk 和 id 是等价的） 是 255 的话，
        # 那么 get_absolute_url 函数返回的就是 /post/255/ ，这样 Article 自己就生成了自己的 URL。
        return reverse('blog:detail',kwargs={'pk':self.pk})

    class Meta:
        #制定文章的排序方式，先按时间排序，后按标题
        ordering = ['-created_time','title']
        verbose_name_plural = u'文章列表'
#阅读量统计
    def increase_reading(self):
        self.reading +=1
        self.save(update_fields=['reading'])
    #摘要截取
    def save(self,*args,**kwargs):
        if not self.excerpt:
            self.excerpt = strip_tags(self.body)[:80] + '...'
        super(Article,self).save(*args,**kwargs)


