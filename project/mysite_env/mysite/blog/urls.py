from django.urls import path
from . import views

#blog
urlpatterns = [
    #http://127.0.0.1:8000/blog/1
    path('<int:blog_pk>', views.blog_detail, name='blog_detail' ),
    path('type/<int:blog_type_pk>', views.blogs_with_type, name='blogs_with_type'),
]