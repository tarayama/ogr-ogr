from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import LineAccount
import urllib
import json
import secrets
import requests
import base64
from ogr.models import Ogr_ogr, Friend
from .forms import LineLinkForm


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
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
    command = ["接続","新規登録","使い方","友達"]
    if event.message.text == "接続":
        Line_user_id = event.source.user_id
        messages = Connect_Django_and_Line(Line_user_id)
    elif event.message.text == "新規登録":
        messages = Make_Django_Account()
    elif event.message.text == "使い方":
        messages = TextSendMessage(text="How to use")
    elif event.message.text == "友達":
        messages = TextSendMessage(text="You have so many friends. I'm so jealous!")
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
            alt_text = "OGR^2",
            template = ButtonsTemplate(
                text = "こちらからアカウントを作成してください。Google Accountをお持ちの方ログインページからそのアカウントを使ってログインすることもできます。",
                title = "新規登録",
                actions = [
                    URIAction(
                        uri="https://ogr-ogr.herokuapp.com/accounts/signup",
                        label="新規登録"
                    ),
                    URIAction(
                        uri="https://ogr-ogr.herokuapp.com/accounts/login",
                        label="Google login"
                    )
                ]
            )
        )
    return messages

def Connect_Django_and_Line(Line_user_id):
    AccountLinkToken = Issue_LineAccountlinkToken(Line_user_id)
    Redirect_UserLinkURL(Line_user_id, AccountLinkToken)
    #接続に成功したメッセージを送信する。
    profile = line_bot_api.get_profile(Line_user_id)
    messages = TextSendMessage(
                        text = 
                            "接続に成功しました。\nこんにちは　{}さん。\n接続解除する場合は「接続解除」と話してください。".format(profile.display_name))
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
                        type = "Account Link",
                        label = "Account Link",
                        uri = "http://ogr-ogr.herokuapp.com/linebot/link/{}/{}".format(Line_user_id,AccountLinkToken)
                    )                    
                ]
            )
        )
    )
    

#3.自社サービスのユーザーIDを取得する
#4.nonceを生成してユーザーをLINEプラットフォームにリダイレクトする
def MakeNonce(): 
    while True:
        nonce = secrets.token_bytes(32)
        nonce = base64.b64encode(nonce)
        noncelist = LineAccount.objects.all()
        for i in noncelist:
            if i.line_nonce != nonce:
                return nonce
            else:
                continue

def get_django_userid_and_redirect_line(request, Line_user_id, linkToken):
    print("linkToken:",linkToken)
    if request.method == 'POST':
        form = LineLinkForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            login(request, user)
            django_userid = user.id
            #4.nonceを生成してユーザーをLINEプラットフォームにリダイレクトする
            nonce = MakeNonce()

            #nonceとユーザーを一緒に保存
            accountlink = LineAccount(
                user = request.user,
                line_userid = Line_user_id,
                line_nonce = nonce,
            )
            accountlink.save()
            redirect_url = "https://access.line.me/dialog/bot/accountLink?linkToken={}&nonce={}".format(linkToken, nonce)
            return redirect(redirect_url)
    else:
        form = LineLinkForm()
    return render(request, 'Linebot/Accountlink.html', {'form': form})


#5.アカウントを連携する

def Disconnect_Django_and_Line():
    return 0

@handler.add(PostbackEvent)
def handle_postback(event):

    UserID = event.source.user_id
    if event.postback.data == 'addfriend':
        pass

    elif event.postback.data == 'friendslist':
        pass

    


