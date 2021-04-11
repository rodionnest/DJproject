# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-datetime')


class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
