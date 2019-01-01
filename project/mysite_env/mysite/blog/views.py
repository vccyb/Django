from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, BlogType

each_page_blogs_number = 5

# Create your views here.

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



def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render_to_response('blog/blog_list.html', context)

def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, id=blog_pk)
    #时间大于 创建晚的
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    #时间小于 创建造的
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    return render_to_response('blog/blog_detail.html', context)

def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type = blog_type )
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type #获取该类型名
    return render_to_response('blog/blogs_with_type.html', context)

def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' %(year, month)
    return render_to_response('blog/blogs_with_date.html', context)

