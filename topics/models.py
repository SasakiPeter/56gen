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

    def throw_three_answer(self):
        return self.answer_set.order_by('votes').reverse()[:3]


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


class Voter(models.Model):
    anonymous = User.objects.get(username="anonymous")
    user = models.ForeignKey(User, verbose_name="投票者",
                             on_delete=models.SET_DEFAULT, default=anonymous.pk)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_answer = models.IntegerField(default=0)
    num_voted = models.IntegerField(default=0)
    contribute_score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.display_name + ': ' + str(self.contribute_score)

    @classmethod
    def calc_cont_sc(cls, num_voted, num_ans):
        if num_voted == 0:
            return 0
        else:
            return num_voted*100//num_ans

    @classmethod
    def exclude_anonymous(cls, queryset):
        return [q for q in queryset if q.user.username != "anonymous"]

    @classmethod
    def update_score(cls, user):
        all_votes = 0
        ans_list = user.answer_set.all()
        for ans in ans_list:
            all_votes += ans.votes
        try:
            score = cls.objects.get(user=user)
        except cls.DoesNotExist:
            score = cls.objects.create(user=user, num_answer=len(
                ans_list), num_voted=all_votes, contribute_score=calc_cont_sc(all_votes, len(ans_list)))
            score.save()
        else:
            score.num_answer = len(ans_list)
            score.num_voted = all_votes
            score.contribute_score = cls.calc_cont_sc(all_votes, len(ans_list))
            score.save()

    @classmethod
    def rank_list(cls):
        user_list = User.objects.all()
        for user in user_list:
            cls.update_score(user)
        score_list = Score.objects.order_by('contribute_score').reverse()
        return cls.exclude_anonymous(score_list)

    def rank(self):
        score_list = self.rank_list()
        for index, score in enumerate(score_list):
            if score.user.id == self.user.id:
                return index + 1
