from django import forms
from .models import Blog_Comment, Blog_Reply



class CommentForm(forms.ModelForm):
    class Meta:
        model = Blog_Comment
        fields = ['comment']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Blog_Reply
        fields = ['reply']