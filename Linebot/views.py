from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import LineAccount
import urllib
import json
#import secrets

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, URIAction
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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    command = ["URL", "友達", "記録の追加", "金額", "お問い合わせ"]
    if (event.message.text == ("URL" or "url")):
        #messages = TextSendMessage(text="https://ogr-ogr.herokuapp.com")
        messages = TemplateSendMessage(
            alt_text="OGR^2",
            template=ButtonsTemplate(
                text="金銭をここで管理しましょう",
                title="OGR^2",
                #image_size="cover",
                #thumbnail_image_url="https://任意の画像URL.jpg",
                actions=[
                    {
                        "type": "uri",
                        "label": "ログイン",
                        "uri": "login"
                    },
                    {
                        "type": "uri",
                        "label": "View detail",
                        "uri": "top"
                    }
                    #URIAction(
                    #    uri="https://ogr-ogr.herokuapp.com",
                    #    label="URL"
                    #)
                ]
            )
        )
    
    elif (event.message.text == ("ログイン")):
        messages = TextSendMessage(text="https://ogr-ogr.herokuapp.com/accounts/login")
    
    else:
        messages = TextSendMessage(
                    text = 
                        """このアプリは友人間での金銭の貸し借りを管理するアプリです。
                        今いくら借りているのか、貸しているのか管理しましょう
                        また、その人に対する貸し借りの可視化もできます""")

    
    reply = line_bot_api.reply_message(
        event.reply_token,
        messages)
        #TextSendMessage(text="今はまだ開発段階のため応答できません"))
        #TextSendMessage(text=event.message.text)) this message is send by user
    return reply



