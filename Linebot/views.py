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

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')


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
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)
        return HttpResponse("ok")
    return HttpResponseBadRequest("error occured")

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
