from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

@login_required(login_url="login")
def create_article(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.author = request.user
            article.order = 100
            article.slug = slugify(article.title)
            article.save()
            return redirect("homepage")
        else:
            return render(request,  'blog/newblog.html', {'article_form': article_form})
    else:
        article_form = ArticleForm()
        return render(request,  'blog/newblog.html', {'article_form': article_form})

@login_required(login_url="login")
def update_article(request, slug):
    
    article = get_object_or_404(Article,slug=slug, author=request.user)
    
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES, instance=article)
        if article_form.is_valid():
            article_form.save()
            return redirect("homepage")
        else:
            return render(request,  'blog/newblog.html', {'article_form': article_form})
    else:
        article_form = ArticleForm(instance=article)
        return render(request,  'blog/newblog.html', {'article_form': article_form})

@login_required(login_url="login")
def list_article(request):
    list_article = request.user.articles.all()

    paginator = Paginator(list_article, 2)  # 5 bài mỗi trang
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj
    }

    return render(request, 'blog/listarticle.html', context)

def view_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comment_form = CommentForm()

    context = {
        'article': article,
        'comment_form': comment_form,

    }
    return render(request, 'blog/articleview.html', context)

@login_required(login_url="login")
def add_comment(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
    return redirect('viewarticle', slug=slug)
