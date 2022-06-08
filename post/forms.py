from django.forms import ModelForm, Textarea, TextInput
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from .models import Comments, Post


class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['body', ]

        widgets = {
            'body': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Comment...",
            })
        }


class PostsForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['user']

        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Title post",
            }),
            'full_text': Textarea(attrs={
                'class': "form-control",
                'placeholder': "All text post",
                'style': 'margin-bottom: 15px;',
            }),
        }


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
