
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
# from django.views import generic
from logging import getLogger, DEBUG, basicConfig
from .forms import LoginForm, SignUpForm, RenameForm
from .models import User
from topics.models import Score

basicConfig()
logger = getLogger(__name__)
logger.setLevel(DEBUG)


def calc_cont_sc(num_voted, num_ans):
    if num_voted == 0:
        return 0
    else:
        return num_voted*100//num_ans


def update_score(user):
    all_votes = 0
    ans_list = user.answer_set.all()
    for ans in ans_list:
        all_votes += ans.votes
    try:
        score = Score.objects.get(user=user)
    except Score.DoesNotExist:
        score = Score.objects.create(user=user, num_answer=len(
            ans_list), num_voted=all_votes, contribute_score=calc_cont_sc(all_votes, len(ans_list)))
        score.save()
    else:
        score.num_answer = len(ans_list)
        score.num_voted = all_votes
        score.contribute_score = calc_cont_sc(all_votes, len(ans_list))
        score.save()


def exclude_anonymous(queryset):
    return [q for q in queryset if q.user.username != "anonymous"]


# ランキング
def index(request):
    user_list = User.objects.all()
    for user in user_list:
        update_score(user)
    score_list = Score.objects.order_by('contribute_score').reverse()
    score_list = exclude_anonymous(score_list)

    page = request.GET.get('page', 1)
    paginator = Paginator(score_list, 10)

    try:
        score_list = paginator.page(page)
    except PageNotAnInteger:
        score_list = paginator.page(1)
    except EmptyPage:
        score_list = paginator.page(paginator.num_pages)

    return render(request, 'accounts/index.html', {'score_list': score_list})


# ユーザー個別ページ
def detail(request, user_id):
    rename_form = RenameForm(request.POST or None)
    user = get_object_or_404(User, pk=user_id)

    if request.method == "GET":
        update_score(user)
        answers = user.answer_set.order_by('votes').reverse()[:3]
        score = get_object_or_404(Score, user=user_id)
        if request.user.is_authenticated and request.user.id == user_id:
            rename_form.fields['display_name'].widget.attrs['value'] = request.user.display_name
            context = {'user': user, 'answers': answers,
                       'score': score, 'rename_form': rename_form}
            return render(request, 'accounts/detail.html', context=context)
        else:
            context = {'user': user, 'answers': answers, 'score': score}
            return render(request, 'accounts/detail.html', context=context)

    if request.method == "POST" and request.user.is_authenticated and request.user.id == user_id and rename_form.is_valid():
        user.display_name = rename_form.cleaned_data['display_name']
        user.save()

    return redirect('accounts:detail', user_id=user_id)


def signin(request):
    login_form = LoginForm(request.POST or None)

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('topics:index')
        else:
            return render(request, 'accounts/signin.html', {'form': login_form})

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('topics:index')
        else:
            message = "不正なログインです。"
            return render(request, 'accounts/signin.html', {'form': login_form, 'error_message': message})


def signout(request):
    if request.method == "POST":
        logout(request)
    return redirect('topics:index')


def signup(request):
    signup_form = SignUpForm(request.POST or None)

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('topics:index')
        else:
            return render(request, 'accounts/signup.html', {'form': signup_form})

    if request.method == "POST" and signup_form.is_valid():
        with transaction.atomic():
            user = signup_form.save(commit=False)
            user.display_name = user.username
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            domain = current_site.domain
            context = {
                'user': user,
                'protocol': request.scheme,
                'domain': domain,
                'token': dumps(user.pk)
            }

            subject_template = get_template(
                'accounts/mail_template/signup/subject.txt')
            subject = subject_template.render()

            message_template = get_template(
                'accounts/mail_template/signup/message.txt')
            message = message_template.render(context)

            user.email_user(subject, message)
        return redirect('accounts:signup_done')
    else:
        return render(request, 'accounts/signup.html', {'form': signup_form})


def signup_done(request):
    return render(request, 'accounts/signup_done.html')


def signup_complete(request, token):
    timeout_secs = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)
    if request.method == "GET":
        try:
            user_pk = loads(token, max_age=timeout_secs)
        except SignatureExpired:
            return HttpResponseBadRequest()
        except BadSignature:
            return HttpResponseBadRequest()
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    login(request, user,
                          backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('topics:index')
    return HttpResponseBadRequest()
