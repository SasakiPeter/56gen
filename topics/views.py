from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from .models import Topic, Answer, Voter
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
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.method == "GET":
        answer_list = topic.answer_set.order_by('votes').reverse()
        context = {'topic': topic, 'answer_list': answer_list,
                   'answer_form': answer_form}
        return render(request, 'topics/detail.html', context)

    if request.method == "POST" and answer_form.is_valid():
        answer = answer_form.save(commit=False)
        answer.topic = topic
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


def vote(request, topic_id):
    if request.method == "POST" and request.user.is_authenticated:
        if 'up' in request.POST:
            ans = get_object_or_404(Answer, pk=request.POST['up'])
            if not Voter.objects.filter(user=request.user.pk, answer=ans.pk).exists():
                ans.votes += 1
                ans.save()
                v = Voter(user=request.user, answer=ans)
                v.save()
        if 'down' in request.POST:
            ans = get_object_or_404(Answer, pk=request.POST['down'])
            if Voter.objects.filter(user=request.user.pk, answer=ans.pk).exists():
                ans.votes -= 1
                ans.save()
                v = Voter.objects.get(user=request.user, answer=ans)
                v.delete()

    return redirect('topics:detail', topic_id=topic_id)


def contact(request):
    if request.method == "POST":
        context = {
            'user': request.user,
            'message': request.POST['contact']
        }

        subject_template = get_template(
            'topics/mail_template/contact/subject.txt')
        subject = subject_template.render()

        message_template = get_template(
            'topics/mail_template/contact/message.txt')
        message = message_template.render(context)

        admin = get_object_or_404(User, email="56gen.operation@gmail.com")
        admin.email_user(subject, message)
        return render(request, 'topics/contact_done.html')

    return render(request, 'topics/contact.html')


def policy(request):
    return render(request, 'topics/policy.html')


def about(request):
    return render(request, 'topics/about.html')

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
