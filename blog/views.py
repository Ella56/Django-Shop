from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,FormView
from .models import Blog, Blog_Comment,Blog_Reply,Tag
from accounts.models import User, Profile
from django.contrib import messages
from product.models import *


# Create your views here.



class BlogView(ListView):
    model = Blog
    template_name = 'blog/blog.html'
    context_object_name = 'blogs'


    def get_queryset(self):
        if self.kwargs.get('tag'):
            return Blog.objects.filter(tags_name=self.kwargs['tag'], status=True).order_by('-created_at')
        return Blog.objects.filter(status=True).order_by('-created_at')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["most_views"] = Blog.objects.filter(status=True).order_by('-total_views')[:4]
        context["most_views_product"] = Product.objects.filter(total_views__gte=0).order_by('-total_views')[:4]
        return context



class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog-post.html'
    context_object_name = 'blog'

    def get(self, request, *args, **kwargs):
        blog = self.get_object()
        blog.total_views += 1
        blog.save()

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['most_views'] = Blog.objects.filter(status=True).order_by('-total_views')[:4]
        context['most_views_product'] = Product.objects.filter(total_views__gte=0).order_by('-total_views')[:4]
        return context