from django.shortcuts import render
from .models import Post, Task


def homepage(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})
