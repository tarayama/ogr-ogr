from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import LineAccount
import urllib
import json
#import secrets
from .models import Ogr_ogr, Friend


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


CHANNEL_ACCESS_TOKEN = 'ZlxbDtTS3SfT9gZjOc8FKgZ+Kkgga9/7VUqfmkb0v3pGOqQFjUA2+A86EJma9riHF32eneBx3fgN+pwEPMRURsbrKOnhWRCo4glIaXfW1W005VUgSEXI7F3wbC0ueR77b0Axq8HgOV2BLZVLJqA9aQdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '4ba709d015f6455475c8aa59369cd88f'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

LINEBOT_ENDPOINT = 'https://api.line.me/v2/bot'
HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + CHANNEL_ACCESS_TOKEN
}

# Create your views here.
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            HttpResponse('Error occured', status=400)
        return HttpResponse('OK', status=200)

def login_again():
    messages = TemplateSendMessage(
            alt_text="OGR^2",
            template=ButtonsTemplate(
                text="こちらからもう一度ログインしなおしてみてください",
                title="エラーが発生しました。",
                actions=[
                    {
                        "type": "uri",
                        "label": "login again",
                        "uri": "https://ogr-ogr.herokuapp.com/accounts/login"
                    }
                ]
            )
        )
    return messages

def reply_message(event, messages):
    reply = line_bot_api.reply_message(
        event.reply_token,
        messages)
        #TextSendMessage(text="今はまだ開発段階のため応答できません"))
        #TextSendMessage(text=event.message.text)) this message is send by user
    return reply

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event, request):
    #command = ["URL", "友達", "記録の追加", "金額", "お問い合わせ"]
    if (event.message.text == ("URL")):
        #messages = TextSendMessage(text="https://ogr-ogr.herokuapp.com")
        messages = TemplateSendMessage(
            alt_text="OGR^2",
            template=ButtonsTemplate(
                text="金銭をここで管理しましょう。",
                title="OGR^2",
                actions=[
                    {
                        "type": "uri",
                        "label": "View detail",
                        "uri": "https://ogr-ogr.herokuapp.com/top/tarayama"
                    }
                ]
            )
        )
    
    elif (event.message.text == ("友達")):
        try:
            friend_list = Friend.objects.filter(user=request.user)
            messages = TextSendMessage(
                            text='Menu',
                            quick_reply=QuickReply(
                                items=[
                                QuickReplyButton(
                                    action=PostbackAction(label="友達一覧", data="friendslist")
                                ),
                                QuickReplyButton(
                                    action=PostbackAction(label="友達の追加", data="addfriend")
                                ),
                            ]))
        except:
            messages = login_again()
    
    elif (event.message.text == ("記録の追加")):
        try:
            ogr_list = Ogr_ogr.objects.Filter(user=request.user)
            friend_list = Friend.objects.filter(user=request.user)
        except:
            pass

    elif (event.message.text == ("金額")):
        try:
            pass
        except:
            pass
    
    
    else:
        messages = TextSendMessage(
                    text = 
                        "このアプリは友人間での金銭の貸し借りを管理するアプリです。\n今いくら借りているのか、貸しているのか管理しましょう\nまた、その人に対する貸し借りの可視化もできます")

    
    #reply = line_bot_api.reply_message(
        #event.reply_token,
        #messages)
        #TextSendMessage(text="今はまだ開発段階のため応答できません"))
        #TextSendMessage(text=event.message.text)) this message is send by user
    return reply_message(event, messages)#reply

@handler.add(PostbackEvent)
def handle_postback(event):

    UserID = event.source.user_id
    if event.postback.data == 'addfriend':
        pass

    elif event.postback.data == 'friendslist':
        pass

    


