from django import forms
from .models import Post, ResponsePost


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'is_published']


class CreateRespondForm(forms.ModelForm):
    class Meta:
        model = ResponsePost
        fields = ['text']