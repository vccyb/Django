# 笔记02

[TOC]





1. 想清楚为啥做网站 兴趣爱好/工作
2. **如何利用django开发网站**
   - 原站的原型：业务流程 功能模块 前端布局 后端模型
   - 具体开发
   - 测试
   - 部署上线
3. 以一个个人博客网站来系统性学习
   - 项目管理
     - IDE	vscode
     - 本地虚拟环境 
     - Git/Github
   - 前端开发
     - html + javascript + CSS
     - jQuery
     - Bootstrap
     - ajax
   - 后端开发
     - 博客的管理和展示
     - 用户的登陆和注册
     - 评论和回复
     - 点赞
   - 数据库和服务器
     - MySQL
     - Linux
     - 网站部署



------

### 简单的构架

网站的功能模块

- 博客
  - 博文
  - 博客分类
  - 博客标签
- 评论
- 点赞
- 阅读
- 用户 -第三方登录

------

### 开启本地虚拟环境

隔开python项目的运行环境

1. 避免python项目库的冲突
2. 完整便捷导出python库的列表

`pip install virtualenv`  安装库

- 创建：virtualenv <环境名>
- 启动：Scripts\activate
- 退出：deactivate

python3.3以上自带虚拟环境功能

`python -m venv name`

其余一样

安装好后pip list可以发现 只有pip 和setuptools两个库 十分的干净

进入虚拟环境后，左上角会显示虚拟环境名

**以下操作在大都在虚拟环境中执行**

------

### 初步创建blog应用

1. 打开blog应用中的model增加博客和博客类型两个模型

```python
from django.db import models
from django.contrib.auth.models import User

class BlogType(models.Model):
    type_name = models.CharField(max_length=20)
    
    def __str__(self):
    	return self.type_name

class Blog(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)# 外键
    author = models.ForeignKey(User, on_delete = models.DO_NOTHING)# 外键
    created_time = models.DateTimeField(auto_now_add = True)
    last_updated_time = models.DateTimeField(auto_now = True)
       
    def __str__(self):
        return "<Blog: %s>" % self.title
    
```

2. 在setting中注册app

3. 先迁移数据库，在创建超级用户

   ```python
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. 修改admin方便后台查看

   ```python
   from django.contrib import admin
   from .models import BlogType, Blog
   
   @admin.register(BlogType)
   class BlogTypeAdmin(admin.ModelAdmin):
       list_display = ('id', 'type_name')
   
   @admin.register(Blog)
   class BlogAdmin(admin.ModelAdmin):
       list_display = ('title', 'blog_type', 'author', 'created_time', 'last_updated_time')
   ```



**补充：pip的一键导出和安装**

导出：`pip freeze > requirements.txt`

安装：`pip install -r requirements.txt`

------



### 继续搭建blog

我们已经建立了blog应用和建立了blog和blogtype两种模型，现在我们让他显示出来

**先显示blog_list页面 和 blog_detail 页面**

1.  设置总分路由

   blog app下新建一个urls.py分路由

   ```python
   from django.urls import path
   from . import views
   #blog
   urlpatterns = [
       path('<int:blog_pk>', views.blog_detail, name='blog_detail' ),
   ]
   ```

   mysite中的总路由

   ```python
   from django.contrib import admin
   from django.urls import path, include
   from blog.views import blog_list
   urlpatterns = [
       path('', blog_list, name='home'),  
       path('admin/', admin.site.urls),
       path('blog/', include('blog.urls')),  #所有localhost:8000/blog/xxx由分路由处理
   ]
   ```

2. 修改blog app 的views.py

   ```python
   from django.shortcuts import render_to_response, get_object_or_404
   from .models import Blog, BlogType  #引用
   
   def blog_list(request):    #主页 
       context = {}
       context['blogs'] = Blog.objects.all()  
       return render_to_response('blog_list.html', context)  #传所有博客
   
   def blog_detail(request, blog_pk): #  localhost:8000/blog/1
       context = {}
       context['blog'] = get_object_or_404(Blog, id=blog_pk)  #传谋篇pk的博客
       return render_to_response('blog_detail.html', context)
   ```

3. 增添模板 在blog app下新建templates模板文件夹 

   - blog_list.html

     ```html
     <!DOCTYPE html>    <!-- localhost:8000 -->
     <html>
     <head>
         <meta charset="UTF-8">
         <title>我的网站</title>
     </head>
     <body>
         <div>
             <a href="{% url 'home' %}"><h3>个人博客网站</h3></a> 
             <!-- home是别名 跳转链接 -->   
         </div>
         <hr>
         {% for blog in blogs %}   
             <a href="{% url 'blog_detail' blog.pk %}"><h3>{{ blog.title }}</h3></a>
         	<p>{{ blog.content|truncatechars:35 }}</p>   
         	<!-- xxx| 是过滤器 -->
         {% empty %}
             <p>-- 暂无博客，敬请期待 --</p>
         {% endfor %}
         <p>一共有{{ blogs|length }}篇博客</p>
     </body>
     </html>
     ```

   - blog_detail.html

     ```html
     <!DOCTYPE html>
     <html>
     <head>
         <meta charset="UTF-8">
         <title>{{ blog.title }}</title>   
     </head>
     <body>
         <div>
             <a href="{% url 'home' %}"> <h3>个人博客网站</h3></a>          
         </div>
         <hr>
         <h3>{{ blog.title }}</h3>  
         <p>作者：{{ blog.author }}</p> 
         <p>发表日期：{{ blog.created_time|date:"Y-m-d H:i:s" }}</p>
         <p>{{ blog.content }}</p>
     </body>
     </html>
     ```

**再设置blog分类的页面**

1. 设置路由 在分路由中

   ```python
   ...     # localhost/blog/type/1
   path('type/<int:blog_type_pk>', views.blogs_with_type, name='blogs_with_type'),
   ```

2. 修改views.py增加方法

   ```python
   ...
   def blogs_with_type(request, blog_type_pk):
       context = {}
       blog_type = get_object_or_404(BlogType, pk=blog_type_pk) 
       context['blogs'] = Blog.objects.filter(blog_type = blog_type ) #获取该类型的博客
       context['blog_type'] = blog_type #获取该类型名
       return render_to_response('blogs_with_type.html', context)
   ```

3. 增加blogs_with_type.html模板

   ```html
   <!DOCTYPE html>  <!--其实和blog_list很像但传递的blogs不同，一个是全部的，一个是特定类型的-->
   <html>
   <head>
       <meta charset="UTF-8">
       <title>{{ blog_type.type_name }}</title> <!-- 修改标题 -->
   </head>
   <body>
       <div>
           <a href="{% url 'home' %}"><h3>个人博客网站</h3></a>          
       </div>
       <hr>    
       <h3>{{ blog_type.type_name }}</h3>
       {% for blog in blogs %}   
           <a href="{% url 'blog_detail' blog.pk %}">
               <h3>{{ blog.title }}</h3> 
           </a>
           <p>{{ blog.content|truncatechars:35 }}</p>   
       {% empty %}
           <p>-- 暂无博客，敬请期待 --</p>
       {% endfor %}
       <p>一共有{{ blogs|length }}篇博客</p>
   </body>
   </html>
   ```

4. 在blog_detail.html模板中新加入博客分类，并让其能够跳转

   ```html
       <p>分类：<a href="{% url 'blogs_with_type'  blog.blog_type.pk %}">{{blog.blog_type}}</a></p>   
   ```

------

### 模板嵌套

三个模板blog_detail.html  blog_list.html  blogs_with_type.html 有大量相同的代码

可以用嵌套模板的方式去做

1. 新建base.html 打洞的是三个模板不相同的地方

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>{% block title %}{% endblock %}</title> <!-- 打洞 名字叫title -->
   </head>
   <body>
       <div>
           <a href="{% url 'home' %}"> 
               <h3>个人博客网站</h3>
           </a>          
       </div>   
       <hr>
       {% block content %}{% endblock %}  <!-- 打洞 名字叫content -->
   </body>
   </html>
   ```

2. 其余模板修改

   比如：blog_detail.html

   ```html
   {% extends 'base.html' %}  <!-- 引用模板 -->
   
   {% block title %}
       {{ blog.title }} 
   {% endblock %}     
   
   {% block content %}
       <h3>{{ blog.title }}</h3>  
       <p>作者：{{ blog.author }}</p> 
       <p>发表日期：{{ blog.created_time|date:"Y-m-d H:i:s" }}</p>
       <p>分类：<a href="{% url 'blogs_with_type'  blog.blog_type.pk %}">{{blog.blog_type}}</a></p>
       <p>{{ blog.content }}</p>
   {% endblock %}
   ```

   其余模板同理修改

   可以对比之前的三个模板，代码节省了很多，更简洁了


**全局模板设置**

全局模板不用管app是否启用

在mysite根目录中创建模板文件夹

在setting中

```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        ...
    },
]
```



**模板文件设置的建议**

如果是封装的特别好，只和app有关系，就放在app里面

如果跟项目有关，就最好放在全局模板



修改后的目录

- blog
- mysite
- templates
  - blog
    - blog_detail.html
    - ...
  - base.html

我们设置的路径从templates开始,所以views找不到

修改views.py

```python
def blog_list(request):
...#return render_to_response('blog_list.html', context) 之前是这样
    return render_to_response('blog/blog_list.html', context)
```



------



### 使用CSS美化页面

1. 页面设计：一般从上到下： 导航栏 主题内容 尾注

2.  增加主页：

   ```python
   urlpatterns = [
       path('', views.home ,name='home'),...]
   ```

3. 在mysite中增加views.py

   ```python
   from django.shortcuts import render_to_response
   def home(request):
       context = {}
       return render_to_response('home.html', context)
   ```

4. 增加home模板

   ```html
   {% extends 'base.html' %}
   {% block title %}
       我的网站|首页
   {% endblock%}
   {% block content %}
       <h3 class="home-content">欢迎访问我的网站</h3>
   {% endblock %}
   ```

5. 使用CSS美化

   - 首页美化

     ```html
     ...
     {% block content %}
         <h3 class="home-content">欢迎访问我的网站</h3>
         <style type="text/css">
             h3.home-content {
                 font-size: 222%;
                 position: absolute;
                 left: 50%;
                 top: 50%;
                 transform: translate(-50%, -50%);
             }
         </style>
     {% endblock %}
     ```

   - 导航栏美化

     ```html
         {% block content %}{% endblock %}
         <style type="text/css">
             body, *{
                 margin: 0;
                 padding: 0;
             }
     
             div.nav{
                 background-color: #eee;
                 border-bottom: 1px solid #ccc;
                 padding: 10px 5px;
                 
             }
     
             div.nav a{
                 text-decoration: none;
                 color: #000;
                 padding: 5px 10px;
             }
     
             a.logo {
                 display: inline-block;
             }        
         </style>
         ...
     ```



**使用静态文件**

CSS文件 ，JS文件，图片

在mysite创建 static文件夹

在static中创建base.html和home.html

在setting中设置

已经有了

```python
STATIC_URL = '/static/'   #网络路由
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),    #设置静态文件的目录
]
```

在home.html 和 base.html中加载静态文件

home.html

```html
{% extends 'base.html' %}
{% load staticfiles %}   <!-- 加载文件 -->

{% block title %}
    我的网站|首页
{% endblock%}

{% block header_extends %}
    <link rel="stylesheet" href="{% static 'home.css' %}">  <!-- 外链样式表 -->
{% endblock %}

{% block content %}
    <h3 class="home-content">欢迎访问我的网站</h3>
{% endblock %}
```

base.html

```html
{% load staticfiles %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'base.css' %}">
    {% block header_extends %}{% endblock %}
</head>
<body>
    <div class="nav">
        <a  class="logo"  href="{% url 'home' %}"> 
            <h3>个人博客网站</h3>
        </a>
        <a href="/">首页</a>
        <a href="{% url 'blog_list' %}">博客</a>
    </div>   

    {% block content %}{% endblock %}

</body>
</html>
```



------

