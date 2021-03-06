from django.forms import ModelForm, BooleanField, TextInput
from django import forms
from allauth.account.forms import SignupForm

from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class PostForm(ModelForm):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control mb-2'}))

    class Meta:
        model = Post
        fields = ['post_type', 'title', 'author', 'text']

class UserForm(ModelForm):
    username = forms.CharField(label='Логин пользователя', widget=forms.TextInput(attrs={'class': 'form-control mb-2 col-md-3'}))
    first_name = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control mb-2 col-md-3'}))
    last_name = forms.CharField(label='Фамилия пользователя', widget=forms.TextInput(attrs={'class': 'form-control mb-2 col-md-5'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user