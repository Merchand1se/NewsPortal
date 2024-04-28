from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class NewForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'author',
            'content',
            'title',
            'postCategory',
        ]


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'author',
            'content',
            'title',
            'postCategory',
        ]