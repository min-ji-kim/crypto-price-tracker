from django import forms
from .models import Post, Comment, Symbol

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('coin_name', 'quantity',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class SymbolForm(forms.ModelForm):

    class Meta:
        model = Symbol
        fields = ('coin_name', 'symbol',)