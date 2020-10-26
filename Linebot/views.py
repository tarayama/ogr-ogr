from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import LineAccount
from flask import Flask, request, abort
import urllib
import json
import secrets

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate
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
            abort(400)
        return HttpResponse('OK', status=200)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply = line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    return reply



