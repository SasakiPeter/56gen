from django.contrib import admin
from .models import Voter, Topic, Answer, Score

admin.site.register(Voter)
admin.site.register(Topic)
admin.site.register(Answer)
admin.site.register(Score)
