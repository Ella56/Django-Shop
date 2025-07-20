from django import forms
from .models import Comment, Reply





class CommentFrom(forms.ModelForm):
   
    class Meta: 
        models = Comment
        fields = ['comment']




class RepliesForm(forms.ModelForm):
    
    class Meta:
        model = Reply
        fields = ['reply']
