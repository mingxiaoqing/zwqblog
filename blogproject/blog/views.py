from django.shortcuts import render,get_object_or_404,HttpResponseRedirect,reverse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
from comments.form import CommentForm
from django.contrib import messages
from django.db.models import Q
import datetime
import markdown
from .models import Article,Category
from users.models import User
from .form import MDEditorForm


class BlogShowView(ListView):
    '''博客展示页面'''
    model = Article
    template_name = 'blog/blog_list.html'
    context_object_name = 'article_list'
    paginate_by = 3

    def get_context_data(self,**kwargs):
        #覆写get_context_data相当于render给模板传递字典变量
        # 首先获得父类生成的传递给模板的字典。
        context = super(BlogShowView,self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator,page,is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:
            #没有分页，不需要显示分页导航
            return {}
        # 当前页左边连续的页码号，初始值为空
        left = []
        right = []
        #第一页页码后不需要省略号
        left_has_more = False
        #最后一页页码前不需要省略号
        right_has_more = False
        first = False
        last = False
        #获取用户当前请求的页码
        page_number = page.number
        # 获得分页后的总页数
        total_pages = paginator.num_pages
        # 获得整个分页页码列表，
        page_range = paginator.page_range
        left = page_range[(page_number-3) if (page_number-3)>0 else 0 :
                          (page_number-1) if (page_number-1)>0 else 0]
        right = page_range[page_number:page_number+3]
        if right:
            if right[-1]<total_pages-1:
                right_has_more=True
            if right[-1]<total_pages:
                last=True
        if left:
            if left[0]>1:
                first=True
            if left[0]>2:
                left_has_more=True

        data = {
                'left':left,
                'right':right,
                'left_has_more':left_has_more,
                'right_has_more':right_has_more,
                'first':first,
                'last':last
        }
        return data


class ArticleDetailView(DetailView):
    '''文章详情页'''
    model = Article
    template_name = 'blog/article_details.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        res = super(ArticleDetailView,self).get(request,*args,**kwargs)
        self.object.increase_reading()
        return res

    def get_object(self, queryset=None):
        article = super(ArticleDetailView,self).get_object(queryset=None)
        article.body=markdown.markdown(article.body,
                                    extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',
                                    ])
        return article

    def get_context_data(self,**kwargs):
    # 覆写 get_context_data 的目的是还要把评论表单、article 下的评论列表传递给模板。
        context = super(ArticleDetailView,self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form':form,
            'comment_list':comment_list
        })
        return context


class ArchivesView(BlogShowView):
    '''按照年份和月来过滤归档'''
    model = Article
    template_name = 'blog/blog_list.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')

        months = [1, 3, 5, 7, 8, 10, 12]
        if int(month) in months:
            dayMax = 31
            return super(ArchivesView, self).get_queryset().filter(
            created_time__range=(datetime.date(int(year), int(month), 1),
                                 datetime.date(int(year), int(month), dayMax)
                                 ))
        elif int(month) ==2:
            if int(year) % 4 ==0 and int(year) % 100 !=0 or int(year) % 400 ==0:
                return super(ArchivesView, self).get_queryset().filter(
                    created_time__range=(datetime.date(int(year), 2, 1),
                                         datetime.date(int(year), 2, 29)
                                         ))
            return super(ArchivesView, self).get_queryset().filter(
                created_time__range=(datetime.date(int(year), 2, 1),
                                     datetime.date(int(year), 2, 28)
                                     ))
        else:
            return super(ArchivesView, self).get_queryset().filter(
                created_time__range=(datetime.date(int(year), int(month), 1),
                                     datetime.date(int(year), int(month), 30)
                                     ))


class CategoryView(BlogShowView):
    '''分类'''
    model = Article
    template_name = 'blog/blog_list.html'
    context_object_name = 'article_list'
    #重写父类方法，该方法获取模型的全部数据

    def get_queryset(self):
        #在类视图中，从 URL 捕获的命名组参数值保存在实例的 kwargs 属性里
        cate = get_object_or_404(Category,pk = self.kwargs.get('pk'))
        #调取父类所有文章列表  再筛选出该分类下的文章列表
        return super(CategoryView,self).get_queryset().filter(category=cate)


class User_article(BlogShowView):
    '''获取当前用户的文章'''
    model = Article
    template_name = 'blog/user_articleList.html'
    context_object_name = 'article_list'
    #重写父类方法，该方法获取模型的全部数据
    def get_queryset(self):
        #在类视图中，从 URL 捕获的命名组参数值保存在实例的 kwargs 属性里
        user1 = get_object_or_404(User,pk = self.kwargs.get('pk'))
        #调取父类所有文章列表  再筛选出该分类下的文章列表
        return super(User_article,self).get_queryset().filter(author=user1)

#简单搜索(备用)
# def search(request):
#     q=request.GET.get('q')
#     error_msg = ''
#     if not q:
#         error_msg = '请输入关键词'
#         return render(request, 'search/search.html', {'error_msg': error_msg})
#     #Q 对象用于包装查询表达式，其作用是为了提供复杂的查询逻辑。
#     article_list = Article.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
#     # article_list = Article.objects.filter(body__icontains = q) or Article.objects.filter(title__icontains=q)
#     # for article in article_list:
#     #      article.body = article.body[0:200]+ '...'
#     return render(request, 'search/search.html', {'error_msg': error_msg,'article_list':article_list})

#增加分类
@login_required
def add_category(request):
    if request.method=='GET':
        return render(request,'blog/add_category.html')
    elif request.method=='POST':
        try:
            category_name = request.POST.get('category_name')
        except:
            return HttpResponseRedirect(reverse('blog:publish'))
        else:
            if Category.objects.filter(name = category_name).first():
                return HttpResponse('已存在此分类')
            category = Category.objects.create(name=category_name)
            category.save()
            return HttpResponseRedirect(reverse('blog:publish'))

#发布文章
@login_required
def Article_publish(request):
    if request.method == 'GET':
        form = MDEditorForm()
        return render(request, 'blog/publish_article.html', {'form':form})
    elif request.method =='POST':
        form = MDEditorForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            # excerpt = form.cleaned_data['excerpt']
            category = form.cleaned_data['category']
            # username = request.session.get('username')
            excerpt = body[0:80]+'...'
            user = User.objects.get(username=request.user.username)
            article = Article.objects.create(body=body,title=title,author=user,category=category, excerpt= excerpt)
            article.save()
            messages.success(request,'恭喜您，文章发布成功')
            return HttpResponseRedirect(reverse('blog:detail',args=(article.pk,)))
        msg='标题或内容不能为空'
        return render(request, 'blog/publish_article.html', {'msg':msg})

#删除文章
@login_required
def Delete_article(request,pk):
    article = Article.objects.filter(pk=pk)
    article.delete()
    messages.success(request,'文章删除成功')
    return HttpResponseRedirect(reverse('blog:list'))

# 编辑文章
@login_required
def Edit_article(request,pk):
    if request.method=='GET':
        article=Article.objects.get(pk=pk)
        return render(request, 'blog/edit_article.html', {'article': article})
    else:
        title = request.POST.get('title')
        body = request.POST.get('body')
        category = request.POST.get('category')
        Article.objects.filter(pk=pk).update(title=title,body=body,category=category)
        messages.success(request, '恭喜您，文章修改成功')
        return HttpResponseRedirect(reverse('blog:detail', args=(pk,)))




