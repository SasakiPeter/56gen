from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Voter, Topic, Answer, Score

admin.site.register(Voter)
admin.site.register(Topic, MarkdownxModelAdmin)
admin.site.register(Answer, MarkdownxModelAdmin)
admin.site.register(Score)
