# 第一周

- python3.7 + Django2.1



### 安装python和Django

1. python去官网下载即可，记得add 到环境目录

2. Django的安装用python的pip工具，进入cmd后

   `pip install Django`

3. 用`pip list` 命令 看是否安装成功





### 入门仪式 hello world

1. 用django创建项目(创建到制定的目录) 

   `django-admin startproject mysite`

2. 关于响应请求

   客户端打开网址，发送请求到服务器，urls处理请求给view，在回应客户端

3. urls的配置

   新建一个views.py（方法）

   ```python 
   from django.http import HttpResponse
   
   def index(request):
       return HttpResponse('Hello world')
   ```

   配置urls(处理网站的请求，给与一个方法index)

   ```python
   from django.contrib import admin
   from django.urls import path
   from .import views
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', views.index),
   ]
   ```

4. 启动服务进入mysite 

   命令`python manage.py runserver`

5. 打开网址127.0.0.1:8000 或则 localhost:8000

6. 创建django项目的用户和密码

   1. 先将自带的数据库migrate`python manage.py migrate` 出现一个db.splite3的文件
   2. `python manage.py createsuperuser`

7. 进入admin管理网页127.0.0.1:8000/admin







### 创建app

命令：`python manage.py starapp article` 创建了一个article的app

创建模型： Article

Article有两个属性 标题和内容 在article的app下的models.py

```python
from django.db import models
class Article(models.Model):  #继承models.Model
    title   = models.CharField(max_length=30) 
    content = models.TextField()
```

**在django项目中注册应用** setting中

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'article',  #注册app
]
```

**同步数据库**

`python manage.py makemigrations`

`python manage.py migrate`

**修改admin，让其在admin中显示**

```python
from django.contrib import admin
from .models import Article #引入模型

admin.site.register(Article) #修改
```

进入admin查看

补充，改中文，进入全局设置setting中

`LANGUAGE_CODE = 'zh-Hans'`







### 使用模板

简单的查看文章的页面：

1. 进行views

   ```python
   from django.shortcuts import render
   from django.http import HttpResponse
   def article_detail(request, article_id): #显示文章详情页
       return HttpResponse("文章id: %s" % article_id) 
   ```

2. 路由urls

   ```python
   from django.contrib import admin
   from django.urls import path
   from .import views
   from article.views import article_detail
   urlpatterns = [
   	...
       path('article/<int:article_id>', article_detail, name="article_detail"),
   ]
   ```

   ```python
   <int:article>可以后去输入网址时跟在article后的那个值
   name是取一个别名
   ```

3. 引用模型：

   补充objects  模型的objects是获取或操作模型的对象

   > Article.objects.get(条件)
   >
   > Article.objects.all()
   >
   > Article.objects.filter(条件)

   在views中

   ```python
   from django.shortcuts import render
   from django.http import HttpResponse
   from .models import Article   #记得引用，相对路径即可
   def article_detail(request, article_id):
       article = Article.objects.get(id=article_id)  #新增 通过id获取article对象
       return HttpResponse("文章标题:%s 文章内容:%s"(article.title,article.content)) 
   ##article有两个对象，一个是title一个是content
   ```

4. 改进，如果用户在输入的过程中输入了不存在的id时，我们给与一个404的反馈

   ```python
   from django.http import HttpResponse, Http404  #引用Http404
   def article_detail(request, article_id):
       try:
           article = Article.objects.get(id=article_id)
       except Article.DoesNotExist:
           raise Http404("Not Exist!")
       return HttpResponse("<h2>文章标题: %s</h2> <br>文章内容: %s" % (article.title,article.content)) 
   ```

   > 这里我们用了python中的try excep方法，当出现不存在的错误DoesNotExit时，给与404反馈

5. **将前后端代码分离，利用templates**

   在app的目录中创建templates文件夹

   在templates中创建模板 article_detail.html

   render就是views中渲染模板的的函数

   在views中

   ```python
   def article_detail(request, article_id):
       try:
           article = Article.objects.get(id=article_id)
           context = {}  #新增
           context['article_obj'] = article #新增
           return render(request, "article_detail.html", context )
       except Article.DoesNotExist:
           raise Http404("Not Exist!")
   ```

   > render三个参数  响应 模板地址 传递的字典

   补充 render_to_response 相当于 render 但不用响应这个参数 只用写两个参数

   ​	get_object_or_404  需要两个参数一个是模型一个是条件

   ```python
   from django.shortcuts import render, render_to_response, get_object_or_404 #引用
   def article_detail(request, article_id):
       article = get_object_or_404(Article, id=article_id) #修改后
       context = {}
       context['article_obj'] = article
       return render_to_response( "article_detail.html", context ) #修改后
   ```

   > 可以对比上面的代码，简洁了不少





### 文章列表

显示出文章的列表

1. 配置urls路由，给定网址

   ```python
   ...
   from article.views import article_detail, article_list #应用article_list方法
   path('article/', article_list, name="article_list")
   ```

2. views

   ```python
   ...
   def article_list(request):
       articles = Article.objects.all() #获取全部文章
       context = {}
       context['articles'] = articles
       return render_to_response( "article_list.html", context) #用模板渲染
   ```

3. article_list.html的编写

   ```html
   <html>
       <head></head>
       <body>
           {% for article in articles %}
               <a href="/article/{{ article.pk }}">{{ article.title }}</a>
           {% endfor %}
       </body>
   </html>
   ```

   注意语法

   改进：**利用urls中配置的别名name**

   ```html
   <html>
       <head></head>
       <body>
           {% for article in articles %}
             <a href="{% url 'article_detail' article.pk %}">{{article.title}}</a>
           {% endfor %}
       </body>
   </html>
   ```



### 总路由和app路由

1. 在app中田间路由文件urls.py

   编写

   ```python
   from django.urls import path
   from . import views
   urlpatterns = [    
       #localhost:8000/article localhost:8000/article/1
       path('<int:article_id>', views.article_detail, name="article_detail"),
       path('', views.article_list, name="article_list")
   ]
   ```

2.  总路由的编写

   ```python
   from django.contrib import admin
   from django.urls import path, include #新增include
   from .import views
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', views.index),
       path('article/', include('article.urls')),
   ]
   ```

   主要就是把app的代码分离开！