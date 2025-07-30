from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Article, Comment, Category


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'content', 'image', 'status', 'order']
        # cách 1: Cách này cũng chạy ngon không #crispy
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'my-title-class'}),
        #     'category': forms.Select(attrs={'class': 'my-category-class'}),
        #     'order': forms.NumberInput(attrs={'class': 'my-order-class'}),
        # }

    # cách 2: Cách này cũng chạy ngon không #crispy
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['category'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['image'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['status'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['order'].widget.attrs.update({'class': 'form-control mb-3'})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control mb-3'})

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
    #         raise forms.ValidationError("Email này đã được sử dụng.")
    #     return email