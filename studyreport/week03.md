# 笔记03

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


