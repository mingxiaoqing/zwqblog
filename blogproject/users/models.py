from django.db import models
#处理注册登录等流程内置模型中导入User  用户模型
from django.contrib.auth.models import AbstractUser
# #重写user

class User(AbstractUser):
    name=models.CharField(max_length=20,verbose_name='姓名')
    nick_name = models.CharField(max_length=30, verbose_name='昵称')
    birday = models.DateField(verbose_name='生日',max_length=20,blank=True,null=True)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=11)
    image = models.ImageField(upload_to='img/%Y/%m',verbose_name='头像')
    sign = models.TextField()


    class Meta(AbstractUser.Meta):
        verbose_name_plural='用户信息'

    def __str__(self):
        return self.username


class OAuthQQ(models.Model):
    '''QQ登录模块'''
    userQQ=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    #QQ关联的openid
    qq_openid = models.CharField(max_length=64,verbose_name='openid')

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name='QQ登录用户数据'
        verbose_name_plural=verbose_name
