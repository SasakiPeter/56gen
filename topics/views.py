from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Answer, Tag
from .forms import AnswerForm, TopicForm

User = get_user_model()


def index(request):
    topic_list = Topic.objects.order_by('pub_date').reverse()
    answer_list = Answer.objects.order_by('votes').reverse()

    page = request.GET.get('topic', 1)
    paginator = Paginator(topic_list, 10)

    try:
        topic_list = paginator.page(page)
    except PageNotAnInteger:
        topic_list = paginator.page(1)
    except EmptyPage:
        topic_list = paginator.page(paginator.num_pages)

    page = request.GET.get('goro', 1)
    paginator = Paginator(answer_list, 10)

    try:
        answer_list = paginator.page(page)
    except PageNotAnInteger:
        answer_list = paginator.page(1)
    except EmptyPage:
        answer_list = paginator.page(paginator.num_pages)

    return render(request, 'topics/index.html', {'topic_list': topic_list, 'answer_list': answer_list})


# 1トピックに対して、複数のゴロが乗っているページ
def detail(request, topic_id):
    answer_form = AnswerForm(request.POST or None)

    if request.method == "GET":
        topic = get_object_or_404(Topic, id=topic_id)
        answer_list = topic.answer_set.order_by('votes').reverse()
        # topic = Topic.objects.get(id=topic_id)
        return render(request, 'topics/detail.html', {'topic': topic, 'answer_list': answer_list, 'answer_form': answer_form})

    if request.method == "POST" and answer_form.is_valid():
        answer = answer_form.save(commit=False)
        answer.topic = Topic.objects.get(id=topic_id)
        if request.user.is_authenticated:
            answer.user = request.user
        answer.save()

    return redirect('topics:detail', topic_id=topic_id)


def build(request):
    topic_form = TopicForm(request.POST or None)

    if request.method == "POST" and topic_form.is_valid():
        topic = topic_form.save(commit=False)
        if request.user.is_authenticated:
            topic.user = request.user
        topic.save()
        topic_form.save_m2m()
        return redirect('topics:index')

    return render(request, 'topics/build.html', {'topic_form': topic_form})

    # tag = Tag.objects.create(name="hoge")
    # q = Topic.objects.create(title="マメ科の生薬覚えられない")

    # q.tags.add(tag) #remove allもある
    # 一括はこう
    # a.tags.set((tag1,tag2)) # clearもある

    # q.save()

    # Topic.objects.filter(tags__name="Django")
    # とかも使いそう

    # 使いそう
    # q.tags.set([Tag.objects.get(name=name)
    #             for name in request.POST.getlist("input-name")])
