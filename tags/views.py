from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from topics.models import Topic
from .models import Tag


def index(request):
    tag_list = Tag.objects.all()
    return render(request, 'tags/index.html', {'tag_list': tag_list})


def detail(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    topic_list = Topic.objects.filter(tags__name=tag.name)

    page = request.GET.get('page', 1)
    paginator = Paginator(topic_list, 5)

    try:
        topic_list = paginator.page(page)
    except PageNotAnInteger:
        topic_list = paginator.page(1)
    except EmptyPage:
        topic_list = paginator.page(paginator.num_pages)

    return render(request, 'tags/detail.html', {'tag': tag, 'topic_list': topic_list})
