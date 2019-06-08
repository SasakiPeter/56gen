from django.contrib import admin
from .models import Tag, Topic, Answer, Score

admin.site.register(Tag)
admin.site.register(Topic)
admin.site.register(Answer)
admin.site.register(Score)
