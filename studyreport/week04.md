# 笔记04

### 博客分类和日期归档对应博客同级

方法1：blog/views.py

```python
...
    #获取对应分类的博客数量
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
    	blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
   		blog_types_list.append(blog_type)
    
    #日期归档对应博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
    	blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                        created_time__month=blog_date.month).count()
    	blog_dates_dict[blog_date] = blog_count
```

方法2：使用annotate注释方法

```
...
from django.db.models import Count
context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
```



模板修改

```python
#在分类归档那块
 <a href="{% url 'blogs_with_type' blog_type.pk %}">
	{{ blog_type.type_name }}({{ blog_type.blog_count }})
</a>
...
#在日期归档出
{% for blog_date, blog_count in blog_dates.items %}
	<li>
		<a href="{% url 'blogs_with_date' blog_date.year blog_date.month %}">
			{{ blog_date|date:"Y年m月" }}({{ blog_count }})
		</a>
	</li>
{% endfor %}
```



------

### 博客后台富文本编辑

- 简单文本编辑
  - 直接贴入html代码
- 富文本编辑
  - 最终解析成html
    - 富文本编辑器
    - markdown编辑器

选择CKeditor

1. 安装：`pip install django-ckeditor`

2. 注册应用 seeting中

3. 配置model 把字段改为RichTextField

   ```python
   class Blog(models.Model):
       ...
       content = RichTextField()
   ```

4. 迁移同步数据库

5. 在模板中修改

   1. detail模板中

      ```html
      blog.content|safe
      ```

   2. list模板中

      ```html
      blog.content|striptags|truncatechars:120
      ```



**增加图片上传功能**

1. 安装pillow库

2. 注册应用ckeditor_uploader 

3. 设置setting

   1. 设置midea

      ```python
      #media
      MEDIA_URL = '/media/'   #路由
      MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  #上传文件夹
      ```

   2. 配置ckeditor

      ```python
      CKEDITOR_UPLOAD_PATH = 'upload/'
      ```

   3. 配置url

      ```python
      from django.contrib import admin
      from django.urls import path, include
      from django.conf import settings
      from django.conf.urls.static import static
      from . import views
      
      urlpatterns = [
          path('', views.home ,name='home'),
          path('admin/', admin.site.urls),
          path('ckeditor', include('ckeditor_uploader.urls')), #新增固定写法
          path('blog/', include('blog.urls')),
      ]
      
      urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
      
      ```

   4. 改字段RichTextField不允许上传改成RichTextUploadingField

      ```python
      from ckeditor_uploader.fields import RichTextUploadingField
      ...
      ```

   5. 数据库迁移即可

------



