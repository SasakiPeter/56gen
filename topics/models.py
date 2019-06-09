from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from tags.models import Tag

User = get_user_model()


class Topic(models.Model):
    title = models.CharField("タイトル", max_length=255)
    text = models.TextField("詳細")
    pub_date = models.DateTimeField('投稿日時', default=timezone.now)
    tags = models.ManyToManyField(Tag, verbose_name="タグ")
    anonymous = User.objects.get(username="anonymous")
    user = models.ForeignKey(User, verbose_name="投稿者", on_delete=models.SET_DEFAULT,
                             default=anonymous.pk)

    def __str__(self):
        return self.title


class Answer(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField("ゴロ", max_length=255)
    desc = models.TextField("説明")
    pub_date = models.DateTimeField('回答日時', default=timezone.now)
    votes = models.IntegerField(default=0)
    anonymous = User.objects.get(username="anonymous")
    user = models.ForeignKey(User, verbose_name="回答者",
                             on_delete=models.SET_DEFAULT, default=anonymous.pk)

    def __str__(self):
        return f"{self.title}: {self.votes}"


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_answer = models.IntegerField(default=0)
    num_voted = models.IntegerField(default=0)
    contribute_score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.display_name + ': ' + str(self.contribute_score)
