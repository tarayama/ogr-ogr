from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ogr_ogr, Friend
from django.http import Http404

# Create your views here.
def index(request):
    #ログイン前トップ
    if request.user.is_authenticated:
        return redirect('top', request.user)
    return render(request, 'ogr/index.html', {})

@login_required
def top(request, user):
    #ログイン後トップ
    ogr_list = Ogr_ogr.objects.filter(user=request.user)
    context = {'ogr_list': ogr_list }
    return render(request, 'ogr/top.html', context)

def update(request, ogr_id):
    friend_list = Friend.objects.filter(user=request.user)
    ogr_detail = Ogr_ogr.objects.get(pk=ogr_id)
    context = {
        'ogr_detail': ogr_detail,
        'friend_list' : friend_list }
    friend = ogr_detail.friends_name
    #if request.method == 'POST':
        
    return render(request, 'ogr/detail.html',context)


def my_page(request, user):
    #マイページ
    ogr_list = Ogr_ogr.objects.filter(user=request.user)
    friend_list = Friend.objects.filter(user=request.user)
    context = {
        'ogr_list' : ogr_list,
        'friend_list' : friend_list}
    return render(request, 'ogr/my_page.html', context)

def addfriend(request):
    friend_list = Friend.objects.filter(user=request.user)
    context = {'friend_list': friend_list }
    if request.method == 'POST':
        for person in friend_list:
            if person.name != request.POST['friend']:
                new_friend = Friend(
                    user = request.user,
                    name = request.POST['friend']
                )
                new_friend.save()
                
        return redirect('top', request.user)
    return render(request, 'ogr/addfriend.html', {})

def create_log(request):
    #記録の作成
    friend_list = Friend.objects.filter(user=request.user)
    context = {'friend_list': friend_list }
    friend = request.user
    if request.method == 'POST':
        for person in friend_list:
            if person.name != request.POST['friends_name']:
                new_friend = Friend(
                    user = request.user,
                    name = request.POST['friends_name']
                )
                new_friend.save()
                friend = new_friend
                break
            elif person.name == request.POST['friends_name']:
                friend = person
        b_or_l_Log = Ogr_ogr(
            user = request.user,
            date = request.POST['date'],
            title = request.POST['title'],
            friends_name = friend,
            money = request.POST['money'],
            detail = request.POST['detail'],
        )
        b_or_l_Log.save()
        return redirect('top', request.user)
    return render(request, 'ogr/create_log.html', context)

def detail(request, ogr_id):
    #詳細
    ogr_detail = Ogr_ogr.objects.get(pk=ogr_id)
    context = {'ogr_detail': ogr_detail }
    return render(request, 'ogr/detail.html',context)

def delete(request, ogr_id):
    #記録の削除
    ogr_detail = Ogr_ogr.objects.get(pk=ogr_id)
    ogr_detail.delete() 
    return redirect('top', request.user)
