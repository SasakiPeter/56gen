from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.files.storage import default_storage
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'ユーザー名/メールアドレス'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label=_('メールアドレス'), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            _('同じメールアドレスが既に登録済みです。'))


class RenameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = "呼び名を入れてください"

    class Meta:
        model = User
        fields = ('display_name',)


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('icon', )
