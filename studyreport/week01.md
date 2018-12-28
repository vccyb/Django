# 第一周

- python3.7 + Django2.1



#### 安装python和Django

1. python去官网下载即可，记得add 到环境目录

2. Django的安装用python的pip工具，进入cmd后

   `pip install Django`

3. 用`pip list` 命令 看是否安装成功





#### 入门仪式 hello world

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





#### 创建app

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









