from django.shortcuts import render
from .models import Tag


def index(request):
    tag_list = Tag.objects.all()
    return render(request, 'tags/index.html', {'tag_list': tag_list})
