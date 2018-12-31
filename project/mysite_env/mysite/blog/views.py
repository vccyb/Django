from django.shortcuts import render_to_response, get_object_or_404
from .models import Blog, BlogType


# Create your views here.

def blog_list(request):
    context = {}
    context['blogs'] = Blog.objects.all()
    context['blog_types'] = BlogType.objects.all()
    # context['blogs_count'] = Blog.objects.all().count()
    return render_to_response('blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, id=blog_pk)
    return render_to_response('blog/blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context['blogs'] = Blog.objects.filter(blog_type = blog_type ) #获取该类型的博客
    context['blog_type'] = blog_type #获取该类型名
    context['blog_types'] = BlogType.objects.all()#获取所有类型
    return render_to_response('blog/blogs_with_type.html', context)


