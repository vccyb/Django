# 笔记02

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
------

### pip的一键导出和安装

导出：`pip freeze > requirements.txt`

安装：`pip install -r requirements.txt`

------

