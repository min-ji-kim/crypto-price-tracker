from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Symbol
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from coinmarketcap import Market
from django.db import *
import urllib3

def symbol_id_list():
    coinmarketcap = Market()
    api_result = coinmarketcap.ticker(start=0, limit=0, convert='krw')
    for coin in api_result:  # loop over arrays
        coin_name = coin['id']
        coin_symbol = coin['symbol']
        symbol = Symbol.objects.create(coin_name=coin_name, symbol=coin_symbol)



# names_dict에 symbol, coin_name을  dictionary 형태로 입력


def get_coin_info(post_result):
    coinmarketcap = Market()
    coin_name_result = ""
    post_result = post_result.upper()

    #print(post_result)
    coin_full_name_queryset = Symbol.objects.filter(symbol=post_result).values('coin_name','symbol')
    if coin_full_name_queryset.exists():
        for coin_name in coin_full_name_queryset:
            coin_name_result = coin_name['coin_name']

    else:
        post_result = post_result.lower()
        coin_full_name_queryset = Symbol.objects.filter(coin_name=post_result).values('coin_name', 'symbol')
        if coin_full_name_queryset.exists():
            for coin_name in coin_full_name_queryset:
                coin_name_result = coin_name['coin_name']
        else:
            coin_name_result = "exception"

    return coin_name_result

def post_list(request):
    user = request.user.id
    posts = Post.objects.filter(published_date__lte=timezone.now(),author_id=user).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

@login_required
def post_update_all(request):
    #symbol_id_list()
    user = request.user.id
    coin_dicts = Post.objects.filter(published_date__lte=timezone.now(), author_id=user).order_by('published_date').values('coin_name', 'quantity', 'id')
    for coin_dict in coin_dicts:
        post = Post.objects.get(published_date__lte=timezone.now(), id=coin_dict['id'])
        coinmarketcap = Market()
        coin = (coinmarketcap.ticker(coin_dict['coin_name'], convert='KRW'))[0]
        post.total_price_krw = float(coin["price_krw"]) * float(coin_dict['quantity'])
        post.price_krw = int(float(coin["price_krw"]))

        print(post.price_krw)
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
    qutntity_check = 0
    if request.method == "POST":
        form = PostForm(request.POST)
        try:
            qutntity_check = isinstance(float(request.POST['quantity']), float)
            if qutntity_check is True:
                qutntity_check = "float"
                print(qutntity_check)
        except Exception:
            qutntity_check = "string"

        coin_name = request.POST['coin_name']
        coin_name = get_coin_info(coin_name)
        if coin_name != "exception" and qutntity_check == "float":
            coinmarketcap = Market()
            coin = (coinmarketcap.ticker(coin_name, convert='KRW'))[0]
            #print(coin)
            if form.is_valid():
                post = form.save(commit=False)
                post.coin_name = coin_name
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
            redirect('post_new')

    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        try:
            qutntity_check = isinstance(float(request.POST['quantity']), float)
            if qutntity_check is True:
                qutntity_check = "float"
                print(qutntity_check)
        except Exception:
            qutntity_check = "string"

        coin_name = request.POST['coin_name']
        coin_name = get_coin_info(coin_name)

        if coin_name != "exception" and qutntity_check == "float":

            coinmarketcap = Market()
            coin = (coinmarketcap.ticker(coin_name, convert='KRW'))[0]
            if form.is_valid():
                post = form.save(commit=False)
                post.coin_name = coin_name
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
            redirect('post_new')

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