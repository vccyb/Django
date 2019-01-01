# 笔记03

[TOC]



### 选择CSS框架

几个方面的考虑：

- 易用性
- 兼容性
- 大小
- 效果
- 功能

选择Bootstrap框架

优点：

- 文档齐全，使用简单
- 兼容较多浏览器
- 非轻量级
- 扁平，简洁
- 组件齐全，响应式



### 下载bootstrap和应用bootstrap

目录结构：

static

- bootstrap-3.3.7

  - css

    - bootstrap.min.css

  - js

    - xxx.js

  - fonts
- base.css
- home.css

修改base.html引用bootstrap

```html
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- 新增 -->
    <meta name="viewport" content="width=device-width, initial-scale=1"> <!-- 新增 -->
    
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'base.css' %}"> 
    <!-- 引用css和js -->
    <link rel="stylesheet" href="{% static 'bootstrap-3.3.7/css/bootstrap.min.css' %}">
    ...
</head>  
<body>
    ...
    <script src="{% static 'jquery-1.12.4.min.js' %}"></script>
    <script src="{% static 'bootstrap-3.3.7/js/bootstrap.min.js' %}"></script>

</body>
```

base.html

```html
{% load staticfiles %}

<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'base.css' %}">
    <link rel="stylesheet" href="{% static 'bootstrap-3.3.7/css/bootstrap.min.css' %}">
    <script type="text/javascript" src="{% static 'jquery-1.12.4.min.js' %}"></script>
    <script type="text/javascript" src="{% static 'bootstrap-3.3.7/js/bootstrap.min.js' %}"></script>
    {% block header_extends %}{% endblock %}
</head>
<body>
    <div class="navbar navbar-default navbar-fixed-top" role="navigation" >
        <div class="container-fluid">
            <div class="navbar-header">
                <a  class="navbar-brand"  href="{% url 'home' %}">个人博客网站</a>
                <button class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar-collapse">        
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>                
                </button>
            </div>
            <div  id="navbar-collapse" class="collapse navbar-collapse" >
                <ul class="nav navbar-nav">
                    <li class="{% block nav_home_active %}{% endblock %}">
                        <a href="{% url 'home' %}">首页</a>
                    </li>
                    <li class="{% block nav_blog_active %}{% endblock %}">
                        <a href="{% url 'blog_list' %}">博客</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
{% block content %}{% endblock %}
</body>
</html>
```

blog增加

```html
{% block nav_blog_active %}active{% endblock %}
```

home增加

```html
{% block nav_home_active %}active{% endblock %}
```



------



### Bootstrap响应式布局

这节课内弄很多，核心就是利用bootstrap优化布局，让页面能看

blog_list.html

```html
{% extends 'base.html' %}
{% block title %}我的网站{% endblock %}
{% load staticfiles %}
{% block header_extends %}
    <link rel="stylesheet" href="{% static 'blog/blog.css' %}">
{% endblock %}
{% block nav_blog_active %}active{% endblock %}
{% block content %}
    <div class="container">
        <div class="row">
            <div class="col-xs-12 col-sm-9 col-md-9 col-lg-10">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        {% block blog_list_title %}博客列表(一共有{{ blogs|length }}篇博客){% endblock %}
                    </div>
                    <div class="panel-body">
                        {% for blog in blogs %}  
                            <div class="blog">
                                <h3>
                                    <a href="{% url 'blog_detail' blog.pk %}">{{ blog.title }}</a>
                                </h3>
                                <ul class="blog-info">
                                    <li>
                                        分类：<a href="{% url 'blogs_with_type' blog.blog_type.pk %}">
                                                {{ blog.blog_type }}</a>
                                    </li>
                                    <li>
                                        <span class="glyphicon glyphicon-time"></span>：{{ blog.created_time|date:"Y-m-d"}}
                                    </li>
                                    
                                </ul>
                                <p>{{ blog.content|truncatechars:35 }}</p>  
                            </div>  
                        {% empty %}
                            <div class="blog">
                                <h3>-- 暂无博客，敬请期待 --</h3>
                            </div>

                            {% endfor %}
                        
                    </div>
                </div>
            </div>

            <div class="hidden-xs col-sm-3 col-md-3 col-lg-2">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h4>博客分类</h4>
                    </div> 
                    <div class="panel-body">
                        <ul class="blog-types">
                            {% for blog_type in blog_types %}
                                <li>
                                    <a href="{% url 'blogs_with_type' blog_type.pk %}">
                                        {{ blog_type.type_name }}
                                    </a>
                                </li>
                            {% empty %}
                                <li></li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>

            </div>
        </div>
    </div>

{% endblock %}
```

blogs_with_type.html

```html
{% extends 'blog/blog_list.html' %}
{% block title %}{{ blog_type.type_name }}{% endblock %}

{% block blog_list_title %}{{ blog_type.type_name }}(一共有{{ blogs|length }}篇博客)
<a href="{% url 'blog_list' %}">查看全部博客</a>
{% endblock %}
```

blog_detail.html

```html
{% extends 'base.html' %}
{% block title %}{{ blog.title }}{% endblock %}
{% block nav_blog_active %}active{% endblock %}

{% load staticfiles %}
{% block header_extends %}
    <link rel="stylesheet" href="{% static 'blog/blog.css' %}">
{% endblock %}

{% block content %}
    <div class="container">
        <div class="row">
            <div class="col-xs-10 col-xs-offset-1">
                <h3>{{ blog.title }}</h3>  
                <ul class="blog-info-description">
                    <li>作者：{{ blog.author }}</li> 
                    <li>发表日期：{{ blog.created_time|date:"Y-m-d H:i:s" }}</li>
                    <li>分类：<a href="{% url 'blogs_with_type'  blog.blog_type.pk %}">{{blog.blog_type}}</a></li>
                </ul>
                <div class="blog-content">{{ blog.content }}</div>
            </div>
        </div>
    </div>
{% endblock %}
```

CSS    blog.css

```css
ul.blog-types{
    list-style-type: none;
}

div.blog h3{
    margin-top: 0.5em;
}

div.blog {
    margin-top: 2em;
    padding-bottom: 1em;
    border-bottom: 1px solid #eee;
}

div.blog:last-child{
    border-bottom: none;
}

div.blog p.blog-info{
    margin-bottom: 0;

}

ul.blog-info{
    list-style-type: none;
    margin-bottom: 2em;
}
ul.blog-info li{
    display: inline-block;
    margin-right: 2em;
}

ul.blog-info-description{
    list-style-type: none;
    margin-bottom: 2em;
}

ul.blog-info-description li{
    display: inline-block;
    margin-right: 2em;
}

div.blog-content{
    text-indent: 2em;
    
}
```



------



### 分页功能

1. 快速添加博客

   **shell 模式添加博客**

   1. python manage.py shell
   2. for 循环执行新增博客代码

   如何添加一片文章？

   1. 先进入shell 出现>>>

      `from blog.models import Blog`

      可用`dir()`查询是否引用了，出现`['Blog', '__builtins__']`即成功引用

   2. 查询现有多少篇博客

      ```cmd
      >>> Blog.objects.all()
      <QuerySet [<Blog: <Blog: 第一篇博客>>, <Blog: <Blog: 新增>>, <Blog: <Blog: 比较长的博客>>, <Blog: <Blog: 随笔2>>, <Blog: <Blog: 超长的博客>>]>
      >>> Blog.objects.count()
      5
      ```

   3. 实例化一个

      ```cmd
      >>> blog = Blog()
      >>> dir()
      ['Blog', '__builtins__', 'blog']
      >>> blog.title = "shell模式下的第一篇"
      >>> blog.content = "XXXXXXXXXXX"
      >>> from blog.models import BlogType
      >>> BlogType.objects.all()
      <QuerySet [<BlogType: Django>, <BlogType: Python>, <BlogType: 日常>]>
      >>> BlogType.objects.all()[0]
      <BlogType: Django>
      >>> blog_type = BlogType.objects.all()[0]
      >>> blog_type
      <BlogType: Django>
      >>> blog.blog_type = blog_type
      >>> from django.contrib.auth.models import User
      >>> User.objects.all()
      <QuerySet [<User: vccyb>]>
      >>> user = User.objects.all()[0]
      >>> blog.author = user
      >>> blog.save()
      >>> Blog.objects.all()
      <QuerySet [<Blog: <Blog: 第一篇博客>>, <Blog: <Blog: 新增>>, <Blog: <Blog: 比较长的博客>>, <Blog: <Blog: 随笔2>>, <Blog: <Blog: 超长的博客>>, <Blog: <Blog: shell模式下的第一篇>>]>
      ```

2. 创建多篇文章

   ```cmd
   >>> for i in range(1,31):
   ...     blog = Blog()
   ...     blog.title = "for %s" %i
   ...     blog.content = "XXXXX:%s" %i
   ...     blog.blog_type = blog_type
   ...     blog.author = user
   ...     blog.save()
   ...
   >>> Blog.objects.all().count()
   36
   ```



**分页**

django自带分页器功能

```cmd
>>> from blog.models import Blog
>>> from django.core.paginator import Paginator
>>> dir()
['Blog', 'Paginator', '__builtins__']
>>> blogs = Blog.objects.all()
>>> blogs.count()
36
>>> paginator = Paginator(blogs, 8)
<string>:1: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'blog.models.Blog'> QuerySet.
```

无法分页的原因是模型没有默认的排序

修改blog

```python
class Blog(models.Model):
...
    class Meta:
        ordering = ['-created_time']
```

记住每次修改模型后都要迁移数据库

```python
python manage.py migtations
python manage.py migrate
```

重新开启本地服务进入shell

```cmd
>>> from django.core.paginator import Paginator
>>> from blog.models import Blog
>>> blogs = Blog.objects.all()
>>> paginator = Paginator(blogs, 8)
>>> paginator
<django.core.paginator.Paginator object at 0x00000299C0861A58>
>>> dir(paginator)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_object_list_is_ordered', '_get_page', 'allow_empty_first_page', 'count', 'get_page', 'num_pages', 'object_list', 'orphans', 'page', 'page_range', 'per_page', 'validate_number']
>>>
```

paginator 有很多功能

几个重要的

```cmd
>>> paginator.count
36
>>> paginator.num_pages
5
>>> paginator.page_range
range(1, 6)


>>> page1 = paginator.page(1)
>>> page1
<Page 1 of 5>
>>> dir(page1)
['__abstractmethods__', '__class__', '__contains__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__weakref__', '_abc_impl', 'count', 'end_index', 'has_next', 'has_other_pages', 'has_previous', 'index', 'next_page_number', 'number', 'object_list', 'paginator', 'previous_page_number', 'start_index']
>>> page1.object_list
<QuerySet [<Blog: <Blog: for 30>>, <Blog: <Blog: for 29>>, <Blog: <Blog: for 28>>, <Blog: <Blog: for 27>>, <Blog: <Blog: for 26>>, <Blog: <Blog: for 25>>, <Blog: <Blog: for 24>>, <Blog: <Blog: for 23>>]>
>>> page1.object_list.count()
8
```

好，我们已经在shell中熟悉了django自带的paginator现在开始设计



1. views.py

   ```python
   ...
   from django.core.paginator import Paginator   #引用分页器
   
   def blog_list(request):
      
       blogs_all_list = Blog.objects.all()
       paginator = Paginator(blogs_all_list, 8) #每8分页
       page_num = request.GET.get('page', 1)   #获取页码参数(GET请求)
       page_of_blogs = paginator.get_page(page_num)
   
       context = {}
       context['blog_all_num'] = blogs_all_list   #所有博客数量
       context['blogs'] = page_of_blogs.object_list #这一页的博客
       context['page_of_blogs'] = page_of_blogs   #这里的page_of_blogs <Page 1 of 5>
       context['blog_types'] = BlogType.objects.all()
       # context['blogs_count'] = Blog.objects.all().count()
       return render_to_response('blog/blog_list.html', context)
   ```

2. 修改模板 blog_list.html

   ```html
   {% block blog_list_title %}博客列表(一共有{{ blog_all_num|length }}篇博客){% endblock %}
   
   <div>
   	<ul class="pagination">
   	<!-- 上一页 -->
   	<li>
   		{% if page_of_blogs.has_previous %}
   			<a href="?page={{ page_of_blogs.previous_page_number }}" aria-label="Previous"><span aria-hidden="true">&laquo;</span>
   			</a>
           {% else %}
                <span aria-hidden="true">&laquo;</span>
           {% endif %}
       </li>
   
   	<!-- 全部页码 -->
   	{% for page_num in page_of_blogs.paginator.page_range %}
   		<li><a href="?page={{ page_num }}">{{ page_num }}</a></li>
       {% endfor %}
                             
       <!-- 下一页 -->
       <li>
       	{% if page_of_blogs.has_next %}
            	<a href="?page={{ page_of_blogs.next_page_number }}" aria-label="Next">
               	<span aria-hidden="true">&raquo;</span></a>
           {% else %}
                   <span aria-hidden="true">&raquo;</span>
           {% endif %}
        </li>
   	 </ul>
   </div>
   ```

3. 其中：

   **page_of_blogs.has_previous**

   **page_of_blogs.next_page_number**

   判断是否有上一页和下一页

   ?page= get请求方法应用



------



### 优化分页展示

1. 当前页高亮
2. 不要显示过多页码

这节课内容巨大，需要好好理解

首先是分页功能的优化

blog_list

```python
  
    blogs_all_list = Blog.objects.all()  #注意和下面对比
    paginator = Paginator(blogs_all_list, each_page_blogs_number) #每8分页
    page_num = request.GET.get('page', 1)   #获取页码参数(GET请求)
    page_of_blogs = paginator.get_page(page_num)

    current_page_num = page_of_blogs.number #获取当前页码
    #获取当前页码前后各两页的页码，并去除非法页码
    page_range = list(range(max(current_page_num-2, 1),current_page_num)) + \
    list(range(current_page_num, min(current_page_num+2, paginator.num_pages)+1 ))

    #加上省略页码标记
    if page_range[0] - 1 >=2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
   
    #加上第一页和尾页
    if page_range[0]!=1:
        page_range.insert(0,1)
    if page_range[-1]!= paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blog_all_num'] = blogs_all_list   #所有博客
    context['blogs'] = page_of_blogs.object_list  #特定页码的博客
    context['page_of_blogs'] = page_of_blogs   #这里的page_of_blogs <Page 1 of 5>
    context['page_range'] = page_range  #  当前页码和前两页后两页，第一页最后一页
```



blogs_with_type

```python
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type = blog_type )
    ...
```

模板修改

```html
<div class="paginator">
	<ul class="pagination">
	<!-- 上一页 -->
		<li>
		{% if page_of_blogs.has_previous %}
			<a href="?page={{ page_of_blogs.previous_page_number }}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a>
		{% else %}
			<span aria-hidden="true">&laquo;</span>
		{% endif %}
		</li>

    <!-- 全部页码 -->
        {% for page_num in page_range %}
        	{% if page_num == page_of_blogs.number %}
        		<li class="active" ><span>{{ page_num }}</span></a></li>
        	{% else %}
        		{% if page_num == '...' %}
        			<li><span>{{ page_num }}</span></li>
        		{% else %}
        			<li><a href="?page={{ page_num }}">{{ page_num }}</a></li>
        		{% endif %}
        	{% endif %}
        {% endfor %}

     <!-- 下一页 -->
        <li>
        	{% if page_of_blogs.has_next %}
        		<a href="?page={{ page_of_blogs.next_page_number }}" aria-label="Next">
        			<span aria-hidden="true">&raquo;</span></a>
        	{% else %}
        		<span aria-hidden="true">&raquo;</span>
        	{% endif %}
        </li>

    </ul>
    <p>
    共有{{ blog_all_num|length }}篇博客，
    当前第{{ page_of_blogs.number }}页，共{{ page_of_blogs.paginator.num_pages }}页
    </p>
</div>
```



这章知识点大家多看看老师的视频了解

------



### 上下篇博客和按月分类

1.  上下篇博客

2. 在博客详细页面的模板blog_detail.html

   ```html
   ...
   <div class="blog-more">
   	<p>上一篇：
   		{% if previous_blog %}
   			<a href="{% url 'blog_detail' previous_blog.pk%}">
                   {{ previous_blog.title }}</a>
           {% else %}
   			暂无
   		{% endif %}
   	</p>
   	<p>下一篇：
   		{% if next_blog %}
   			<a href="{% url 'blog_detail' next_blog.pk%}">
   				{{ next_blog.title }}</a>
   		{% else %}
   			暂无
   		{% endif %}
   	</p>
   </div>
   ```

3. views.py 修改blog_detail方法

   ```python
   def blog_detail(request, blog_pk):
       context = {}
       blog = get_object_or_404(Blog, id=blog_pk)
       #时间大于 创建晚的
       context['previous_blog'] = 		 Blog.objects.filter(created_time__gt=blog.created_time).last()
       #时间小于 创建造的
       context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
       context['blog'] = blog
       return render_to_response('blog/blog_detail.html', context)
   ```

   这样传递前后篇博客



代码优化：将重复的代码写成函数使用比如分页功能就是重复代码

```python
def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, each_page_blogs_number) #每8分页
    page_num = request.GET.get('page', 1)   #获取页码参数(GET请求)
    page_of_blogs = paginator.get_page(page_num)

    current_page_num = page_of_blogs.number #获取当前页码
    #获取当前页码前后各两页的页码，并去除非法页码
    page_range = list(range(max(current_page_num-2, 1),current_page_num)) + \
    list(range(current_page_num, min(current_page_num+2, paginator.num_pages)+1 ))

    #加上省略页码标记
    if page_range[0] - 1 >=2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
   
   
    #加上第一页和尾页
    if page_range[0]!=1:
        page_range.insert(0,1)
    if page_range[-1]!= paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blog_all_num'] = blogs_all_list
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs   #这里的page_of_blogs <Page 1 of 5>
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")
    return context
```

这了将几个功能集成在了一起

1. 分页功能和美化分页

2. 获取所有博客数量 获取类型归档和时间归档

3. 获取归档后列表显示的博客

4. 功能集成后剩下函数只需要引用即可

   ```python
   def blog_list(request):
       blogs_all_list = Blog.objects.all()
       context = get_blog_list_common_data(request, blogs_all_list)
       return render_to_response('blog/blog_list.html', context)
       
   def blogs_with_type(request, blog_type_pk):
       blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
       blogs_all_list = Blog.objects.filter(blog_type = blog_type )
       context = get_blog_list_common_data(request, blogs_all_list)
       context['blog_type'] = blog_type #获取该类型名
       return render_to_response('blog/blogs_with_type.html', context)
      
     
   def blogs_with_date(request, year, month):
   	blogs_all_list = 	Blog.objects.filter(created_time__year=year,created_time__month=month)
       context = get_blog_list_common_data(request, blogs_all_list)
       context['blogs_with_date'] = '%s年%s月' %(year, month)
       return render_to_response('blog/blogs_with_date.html', context)
   ```

时间归档与类型归档很像，可以参考写法

在新建blogs_with_date.html

```html
{% extends 'blog/blog_list.html' %}
{% block title %}日期归档：{{ blogs_with_date }}{% endblock %}

{% block blog_list_title %}{{ blog_type.type_name }}
    日期归档：{{ blogs_with_date }}
    <a href="{% url 'blog_list' %}">查看全部博客</a>
{% endblock %}
```

在博客的分路由中设置路由

```python
...
path('type/<int:blog_type_pk>', views.blogs_with_type, name='blogs_with_type'),
path('date/<int:year>/<int:month>', views.blogs_with_date, name='blogs_with_date'),
```



------

