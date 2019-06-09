from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from django.utils.html import mark_safe
from .models import Answer, Topic, Tag


class AnswerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

        self.fields['tags'].widget = MyCheckboxSelectMultiple()
        self.fields['tags'].queryset = Tag.objects
        # self.fields['tags'].widget.attrs['class'] = 'form-check-input'

    class Meta:
        model = Topic
        fields = ('title', 'text', 'tags')
