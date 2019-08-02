from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from django.utils.html import mark_safe
from markdownx.widgets import MarkdownxWidget
from .models import Answer, Topic, Tag


class AnswerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['desc'].widget = MarkdownxWidget()
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model = Answer
        fields = ('title', 'desc')


class MyCheckboxSelectMultiple(CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        html = super(MyCheckboxSelectMultiple, self).render(
            name, value, attrs, renderer)
        return mark_safe(html.replace('<li>', '<li class="from-check form-check-inline">'))


class TopicForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget = MarkdownxWidget()
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
        self.fields['text'].initial = """## マークダウンの書き方
### 順序なしリスト

* リストアイテム1
* リストアイテム2
* リストアイテム3

### 順序ありリスト

1. リストアイテム
1. リストアイテム
1. リストアイテム

### 文字強調

*イタリック*  
**太文字**

### 引用

> #### コラム~マークダウンとは
> このサイトでは[マークダウン形式](https://ja.wikipedia.org/wiki/Markdown)での入力を受け付けています。
> 上記に例を示したので、例にならって入力してみてください。"""
        self.fields['tags'].widget = MyCheckboxSelectMultiple()
        self.fields['tags'].queryset = Tag.objects
        # self.fields['tags'].widget.attrs['class'] = 'form-check-input'

    class Meta:
        model = Topic
        fields = ('title', 'text', 'tags')
