from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from ogr.models import Ogr_ogr, Friend
from ogr.plot import *
from .models import LineAccount
import json
import secrets
import requests
import base64

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ImageSendMessage,
    ButtonsTemplate, URIAction,
    PostbackEvent, PostbackTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackAction,
    MessageAction
    
)
import os

try:
    import Linebot.environment_valiable
except:
    pass

LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
#print("token:",LINE_CHANNEL_ACCESS_TOKEN)
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']
#print("secret:",LINE_CHANNEL_SECRET)

LINEBOT_ENDPOINT = 'https://api.line.me/v2/bot'
HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + LINE_CHANNEL_ACCESS_TOKEN
}

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
print("line_bot_api",line_bot_api)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
print("handler",handler)

# Create your views here.
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        print("signature:",signature)
        body = request.body.decode('utf-8')
        print("body", body)
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            return HttpResponse('Error occured', status=400)
        return HttpResponse('OK', status=200)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event, request):
    command = ["接続","新規登録","使い方","友達","接続解除", "ステータス"]
    Line_user_id = event.source.user_id
    if event.message.text == "接続":
        messages = Connect_Django_and_Line(Line_user_id)
    elif event.message.text == "新規登録":
        messages = Make_Django_Account()
    elif event.message.text == "使い方":
        messages = TextSendMessage(text="How to use")
    elif event.message.text == "友達":
        messages = reply_FriendList(Line_user_id)
    elif event.message.text == "接続解除":
        messages = Disconnect_Django_and_Line(Line_user_id)
    elif event.message.text == "ステータス":
        try:
            account = LineAccount.objects.get(line_userid=Line_user_id)
            profile = line_bot_api.get_profile(Line_user_id)
            messages = TextSendMessage(text="こんにちは。\n{}/{}さん\nあなたのLINEアカウントはOGR^2との接続が完了しています。".format(profile.display_name, account.user.username))
        except:
            messages = TextSendMessage(text="あなたのLINEアカウントはOGR^2と未連携です。")
    else:
        messages = Normal_Reply_Message()

    reply = line_bot_api.reply_message(
        event.reply_token,
        messages)
        #TextSendMessage(text=event.message.text)) this message is send by user
    return reply

def Normal_Reply_Message():
    messages = TextSendMessage(
                        text = 
                            "このアプリは友人間での金銭の貸し借りを管理するアプリです。\n今いくら借りているのか、貸しているのか管理しましょう\nまた、その人に対する貸し借りの可視化もできます")
    return messages

def Make_Django_Account():
    messages = TemplateSendMessage(
            alt_text = "Register account",
            template = ButtonsTemplate(
                text = "こちらから新規登録してください。\nログインページからGoogle Accountでログインすることもできます。",
                title = "新規登録",
                actions = [
                    URIAction(
                        label = "新規登録",
                        uri = "http://ogr-ogr.herokuapp.com/accounts/signup"
                    )                    
                ]
            )
        )
    return messages
    

def Connect_Django_and_Line(Line_user_id):
    AccountLinkToken = Issue_LineAccountlinkToken(Line_user_id)
    Redirect_UserLinkURL(Line_user_id, AccountLinkToken)
    #接続中メッセージを送信する。
    profile = line_bot_api.get_profile(Line_user_id)
    messages = TextSendMessage(text = "接続中です\n接続が完了したら「ステータス」と話しかけて完了を確認してください。")
    return messages

#1.連携トークンを発行する
def Issue_LineAccountlinkToken(Line_user_id):
    token_url  = "https://api.line.me/v2/bot/user/{}/linkToken".format(Line_user_id)
    headers = {
        'Authorization' : "Bearer {}".format(LINE_CHANNEL_ACCESS_TOKEN)
    }
    response = requests.post(token_url, headers=headers)
    values = json.loads(response.text)
    AccountLinkToken = values['linkToken']
    return AccountLinkToken

#2.ユーザーを連携URLにリダイレクトする
def Redirect_UserLinkURL(Line_user_id, AccountLinkToken):
    line_bot_api.push_message(
        Line_user_id,
        TemplateSendMessage(
            alt_text = "Account Link",
            template = ButtonsTemplate(
                text = "Account Link",
                title = "Account Linkを実行する",
                actions = [
                    URIAction(
                        label = "Account Link",
                        uri = "https://ogr-ogr.herokuapp.com/linebot/link/{}/{}".format(Line_user_id,AccountLinkToken)
                    )                    
                ]
            )
        )
    )
    

#3.自社サービスのユーザーIDを取得する
#4.nonceを生成してユーザーをLINEプラットフォームにリダイレクトする
def MakeNonce(Line_user_id): 
    nonce = secrets.token_bytes(32)
    nonce = base64.b64encode(nonce)
    print("Make nonce:",nonce)
    #Line_useridが既に存在するのかチェック
    #既にnonceが存在するのかのチェック
    for i in LineAccount.objects.all():
        print(i)
        if Line_user_id == i.line_userid:
            print("このLINEIDは既に登録されています。")
            line_bot_api.push_message(
                Line_user_id,
                TextSendMessage(
                            text = 
                                "既にこのLINEIDは登録されています。登録解除する場合は「接続解除」またはブロックしてください。"
                )
            )
            nonce = "500"
            return nonce
        if nonce == i.line_nonceToken:
            print("このnonceは他のユーザーのnonceとかぶっています。")
            MakeNonce()
    #存在しない場合、nonceを返す
    return nonce

def get_django_userid_and_redirect_line(request, Line_user_id, linkToken):
    if request.method == 'POST':
        print("Line_user_id:", Line_user_id)
        print("linkToken:",linkToken)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print('ログインに成功しました')
            else:
                print('ログインに失敗しました')
                return HttpResponse('エラーが発生しました。ログインに失敗した可能性があります。', status=400)
                
        else:
            return HttpResponse('エラーが発生しました。アカウントが存在しません。 <a href ="https://ogr-ogr.herokuapp.com/accounts/signup/">こちら</a>からアカウントを作成してください。', status=400)
        django_userid = user.id
        #4.nonceを生成してユーザーをLINEプラットフォームにリダイレクトする
        nonce = MakeNonce(Line_user_id)
        print("nonce:",nonce)
        if nonce == "500":
            return HttpResponse('エラーが発生しました。既に登録されています。', status=400)                
        #nonceとユーザーを一緒に保存
        accountlink = LineAccount(
            user = request.user,
            line_userid = Line_user_id,
            line_nonceToken = nonce,
        )
        accountlink.save()
        print("Success!")
        #5.アカウントを連携する
        redirect_url = "https://access.line.me/dialog/bot/accountLink?linkToken={}&nonce={}".format(linkToken, nonce)
        return redirect(redirect_url)
    return render(request, 'Linebot/AccountLink.html', {})

#DjangoとLINEの接続解除
def Disconnect_Django_and_Line(Line_user_id):
    profile = LineAccount.objects.get(line_userid=Line_user_id)
    profile.delete()
    messages = TextSendMessage(text="接続解除しました。")
    return messages

def reply_FriendList(Line_user_id):
    try:
        account = LineAccount.objects.get(line_userid=Line_user_id)
        friend_list = Friend.objects.filter(user=account.user)
        columns = []
        for friend in friend_list:
            print("friend_name", friend.name)
        
            columns.append(
                CarouselColumn(
                    text = "グラフを表示したい友達を選択してください",
                    title = "友達一覧",
                    actions = [
                        PostbackAction(
                            label=friend.name,
                            data=friend.name
                        )
                    ]
                )
            )
            
        columns.append(
            CarouselColumn(
                text = "グラフを表示したい友達を選択してください",
                title = "友達一覧",
                actions = [
                    URIAction(
                        label = "友達登録",
                        uri = "https://ogr-ogr.herokuapp.com/addfriend"
                    )
                ]
            )
        )
        #print("columns", columns)

        friend_list = list(Friend.objects.filter(user=account.user))
        message = TemplateSendMessage(
            alt_text = "友達を選択してください",
            template = CarouselTemplate(
                columns = columns
            )
        )
        
    except:
        message = TemplateSendMessage(
            alt_text = "友達登録",
            template = ButtonsTemplate(
                text = "こちらから友達の登録を行ってください",
                title = "現在あなたの友達が登録されていません",
                actions = [
                    URIAction(
                        label = "友達登録",
                        uri = "https://ogr-ogr.herokuapp.com/addfriend"
                    )                    
                ]
            )
        )
    return message

#友人との貸し借り金額のグラフを返す
def reply_FriendMoneyPlot(Line_user_id, postbackdata):
    account = LineAccount.objects.get(line_userid=Line_user_id)
    friend_list = Friend.objects.filter(user=account.user)
    for friend in friend_list:
        if postbackdata == friend.name:
            friendevent = Ogr_ogr.objects.filter(friends_name__name=friend.name)
            event = FriendEvent(friendevent)
            datelist = event.getDatelist()
            datelist = list(dict.fromkeys(datelist))
            moneylist = event.getMoneyList()
            png = event.plot(datelist, moneylist, friend.name)
            imgurl = "https://ogr-ogr.herokuapp.com/mypage/{}/friends/{}/plot".format(account.user.name, friend.name)
            print("image url:", imgurl)
            image_message = ImageSendMessage(
                original_content_url = imgurl,
                preview_image_url = imgurl
            )
            break
    return image_message

@handler.add(PostbackEvent)
def handle_postback(event):
    Line_user_id = event.source.user_id
    postbackdata = event.postback.data
    if postbackdata == '友達登録':
        pass

    else:
        messages = reply_FriendMoneyPlot(Line_user_id, postbackdata)
    reply = line_bot_api.reply_message(
        event.reply_token,
        messages)
    return reply

    


