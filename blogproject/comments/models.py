from django.db import models

class Comment(models.Model):
    name = models.ForeignKey('users.User')
    text = models.TextField(max_length=500)
    created_time = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey('blog.Article')
    class Meta:
        verbose_name_plural='评论列表'


class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    subject=models.CharField(max_length=30)
    message = models.TextField()
    class Meta:
        verbose_name_plural='用户留言'