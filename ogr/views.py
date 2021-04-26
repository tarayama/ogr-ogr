from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ogr_ogr, Friend
from django.http import Http404, HttpResponse
import matplotlib
import matplotlib.pyplot as plt
from .plot import *
import io
from django.views.decorators.csrf import requires_csrf_token

# Create your views here.
def index(request):
    #ログイン前トップ
    if request.user.is_authenticated:
        return redirect('top')
    return render(request, 'ogr/index.html', {})

@login_required
def top(request):
    #ログイン後トップ
    ogr_list = Ogr_ogr.objects.filter(user=request.user).order_by('-date')
    context = {'ogr_list': ogr_list }
    return render(request, 'ogr/top.html', context)

@login_required
def edit(request, ogr_id):
    friend_list = Friend.objects.filter(user=request.user)
    ogr_detail = Ogr_ogr.objects.get(pk=ogr_id)
    context = {
        'ogr_detail': ogr_detail,
        'friend_list' : friend_list }
    if request.method == 'POST':
        same_friend = Friend.objects.get(id=int(request.POST['friends_name']))
        ogr_detail.date = request.POST['date']
        ogr_detail.title = request.POST['title']
        ogr_detail.friends_name = same_friend
        ogr_detail.money = request.POST['money']
        ogr_detail.detail = request.POST['detail']
        ogr_detail.save()
    
        return redirect('detail',ogr_id)
        
    return render(request, 'ogr/edit.html',context)

@login_required
def my_page(request):
    #マイページ
    ogr_list = Ogr_ogr.objects.filter(user=request.user)
    friend_list = Friend.objects.filter(user=request.user)
    context = {
        'ogr_list' : ogr_list,
        'friend_list' : friend_list}
    return render(request, 'ogr/my_page.html', context)

@login_required
def addfriend(request):
    friend_list = Friend.objects.filter(user=request.user)
    context = {'friend_list': friend_list }
    friend = ""
    if request.method == 'POST':
        for person in friend_list:
            if person.name == request.POST['friend']: 
                if person.user == request.user:
                    return HttpResponse("エラー：既に登録されている名前です。他の名前をご利用ください")

        new_friend = Friend(
            user = request.user,
            name = request.POST['friend']
        )
        new_friend.save()   
                
        return redirect('top')
    return render(request, 'ogr/addfriend.html', {})


@login_required
def create_log(request):
    #記録の作成
    friend_list = Friend.objects.filter(user=request.user)
    context = {'friend_list': friend_list }
    
    if request.method == 'POST':
        same_friend = Friend.objects.get(id=int(request.POST['friends_name']))
        b_or_l_Log = Ogr_ogr(
            user = request.user,
            date = request.POST['date'],
            title = request.POST['title'],
            friends_name = same_friend,
            money = request.POST['money'],
            detail = request.POST['detail'],
        )
        b_or_l_Log.save()
        return redirect('top', request.user)
    return render(request, 'ogr/create_log.html', context)

@login_required
def detail(request, ogr_id):
    #詳細
    ogr_detail = Ogr_ogr.objects.get(user=request.user, pk=ogr_id)
    context = {'ogr_detail': ogr_detail }
    if request.method == 'POST':
        if request.POST['solution'] == '1':
            ogr_detail.solution = 1
        elif request.POST['solution'] == '0':
            ogr_detail.solution = 0
        ogr_detail.save()
        return redirect('detail',ogr_id)
    return render(request, 'ogr/detail.html',context)

@login_required
def delete(request, ogr_id):
    #記録の削除
    ogr_detail = Ogr_ogr.objects.get(user=request.user, pk=ogr_id)
    ogr_detail.delete() 
    return redirect('top', request.user)


def plot_log(request, friendid):
    try:
        friendevent = Ogr_ogr.objects.filter(user=request.user, friends_name__id=friendid)
        friend = Friend.objects.get(user=request.user, id=friendid)
        friendname = friend.name
    except:
        return HttpResponse("Not Found (404)あなたのアカウントか指定された友達が見つかりません", status=404)
    user = request.user
    event = FriendEvent(user, friendevent)
    datelist = event.getDatelist()
    datelist = list(dict.fromkeys(datelist))
    moneylist = event.getMoneyList()
    plt.rcParams['font.family'] = 'Yu Mincho'
    png = event.plot(datelist, moneylist, friendname)
    return HttpResponse(png, content_type='image/png')    

@login_required
def friend_log(request, friendid): 
    ogr_list = Ogr_ogr.objects.filter(user=request.user, friends_name__id=friendid)
    friend = Friend.objects.get(user=request.user, id=friendid)
    event = FriendEvent(request.user, ogr_list)
    totalmoney = event.getTotalMoney()
    context = {
        'ogr_list' : ogr_list,
        'friend' : friend,
        'totalmoney' : totalmoney
        }
    return render(request, 'ogr/friend_log.html', context)
