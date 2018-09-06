from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.http import HttpResponseRedirect
from blog.models import Article
from .form import CommentForm
from .models import Contact
from users.models import User
from django.contrib import messages


def article_comment(request,article_pk):
    #Article存在就获取  否则返回404
    article = get_object_or_404(Article,pk=article_pk)
    if request.method=='POST':
        #用户提交的数据保存在request.POST中，这是一个类字典对象
        form = CommentForm(request.POST)
        if form.is_valid():
            # commit=False 的作用是仅仅利用表单的数据
            # 生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)
            #把评论和被评论的文章关联起来
            comment.article = article
            comment.name= User.objects.get(username=request.user)
            comment.save()
            # 重定向到 article 的详情页，实际上当 redirect 函数接收一个模型的实例时，
            # 它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(article)
        else:
            #获取article下的所有评论
            #等效于Comment.objects.filter(article=article)
            #通过外键关联，的类，可以调用**_set属性来获取所有;
            # ** 为关联模型的类名（小类）
            comment_list = article.comment_set.all()
            context = {
                'article':article,
                'form':form,
                'comment_list':comment_list
            }
            return render(request, 'blog/article_details.html', context=context)
    return redirect(article)


def contact(request):
    if request.method == 'GET':
        return render(request,'index.html')
    elif request.method == 'POST':
        try:
            name = request.POST.get('contact_name')
            email = request.POST.get('contact_email')
            subject = request.POST.get('contact_subject')
            message = request.POST.get('contact_message')
        except:
            msg = '内容有误，请重新填写'
            return render(request, 'index.html', {'msg': msg})
        con = Contact.objects.create(name=name,email=email,subject=subject,message=message)
        con.save()
        msg = '信息提交成功,感谢您的支持'
        return render(request,'index.html',{'msg':msg})




