from django.forms import ModelForm, BooleanField, TextInput
from .models import Post
from django import forms


class PostForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control mb-2'}))

    class Meta:
        model = Post
        fields = ['post_type', 'title', 'author']
