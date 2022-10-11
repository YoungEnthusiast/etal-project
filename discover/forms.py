from django import forms
from .models import Comment, Post

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('post_type', 'body',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class SearchForm(forms.Form):
    query = forms.CharField()
