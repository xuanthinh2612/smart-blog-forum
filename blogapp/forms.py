from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Article, Comment, Category


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'content', 'image', 'status']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
    #         raise forms.ValidationError("Email này đã được sử dụng.")
    #     return email