from django import forms
from .models import Comment, Reply





class CommentFrom(forms.ModelForm):
   
    class Meta: 
        model = Comment
        fields = ['comment']




class RepliesForm(forms.ModelForm):
    
    class Meta:
        model = Reply
        fields = ['reply']
