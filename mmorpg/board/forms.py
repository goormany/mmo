from django import forms
from .models import Post, ResponsePost
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CreatePostForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'is_published']


class CreateRespondForm(forms.ModelForm):
    class Meta:
        model = ResponsePost
        fields = ['text']