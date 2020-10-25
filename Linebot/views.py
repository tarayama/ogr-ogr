from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
import json
from django.views.decorators.csrf import csrf_exempt
from .message import *

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

CHANNEL_ACCESS_TOKEN = 'ZlxbDtTS3SfT9gZjOc8FKgZ+Kkgga9/7VUqfmkb0v3pGOqQFjUA2+A86EJma9riHF32eneBx3fgN+pwEPMRURsbrKOnhWRCo4glIaXfW1W005VUgSEXI7F3wbC0ueR77b0Axq8HgOV2BLZVLJqA9aQdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET ='4ba709d015f6455475c8aa59369cd88f'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


# Create your views here.
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        #request = json.loads(request.body.decode('utf-8'))
        #events = request['events']
        #for event in events:
        #    message = event['message']
        #    reply_token = event['replyToken']
        #    line_message = LineMessage(create_message(message['text']))
        #    line_message.reply(reply_token)
        # return HttpResponse("ok")
        signature = request.headers['X-Line-Signature']
        # get request body as text
        body = request.get_data(as_text=True)
        print("body:",body,"\n")
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)
        return "ok"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
