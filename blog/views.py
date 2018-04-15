from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from coinmarketcap import Market
from django.db import *
import urllib3

def post_list(request):
    user = request.user.id
    posts = Post.objects.filter(published_date__lte=timezone.now(),author_id=user).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

@login_required
def post_update_all(request):
    user = request.user.id
    coin_dicts = Post.objects.filter(published_date__lte=timezone.now(), author_id=user).order_by('published_date').values('coin_name', 'quantity', 'id')
    for coin_dict in coin_dicts:
        #print(coin_dict['coin_name'], coin_dict['quantity'], coin_dict['id'])
        #print(type(coin_dict['coin_name']), coin_dict['quantity'], coin_dict['id'])
        post = Post.objects.get(published_date__lte=timezone.now(), id=coin_dict['id'])
        coinmarketcap = Market()
        coin = (coinmarketcap.ticker(coin_dict['coin_name'], convert='KRW'))[0]

        post.total_price_krw = float(coin["price_krw"]) * float(coin_dict['quantity'])
        post.price_krw = coin["price_krw"]
        post.price_usd = coin["price_usd"]
        post.price_btc = coin["price_btc"]
        post.author = request.user
        post.publish()
        post.save()
        print(post.coin_name, post.total_price_krw, post.price_krw )

    posts = Post.objects.filter(published_date__lte=timezone.now(),author_id=user).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        coin_name = request.POST['coin_name']
        coinmarketcap = Market()
        coin = (coinmarketcap.ticker(coin_name, convert='KRW'))[0]
        if form.is_valid():
            post = form.save(commit=False)
            post.total_price_krw = float(coin["price_krw"]) * float(request.POST['quantity'])
            post.price_krw = coin["price_krw"]
            post.price_usd = coin["price_usd"]
            post.price_btc = coin["price_btc"]
            post.symbol = coin["symbol"]
            post.author = request.user
            post.publish()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

#@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)