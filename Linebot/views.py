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

try:
    from config.local_settings import *
except ImportError:
    CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
    CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

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
def Connect_LineAccount(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    line_userid = profile.userid
    getToken = "{}/user/{}/linkToken".format(LINEBOT_ENDPOINT,line_userid)
    messages = [{
        "type": "template",
        "altText": "Account Link",
        "template": {
            "type": "buttons",
            "text": "Account Link",
            "actions": [{
                "type": "uri",
                "label": "Account Link",
                "uri": "https://ogr-ogr.herokuapp.com/accounts/login"
            }]
        }
    }]
    ogr_userid = push_message(line_userid, messages)
    if ogr_userid == request.user.id:
        lineaccount = LineAccount(
            user = request.user,
            line_userid = line_userid,
            line_nonceToken = make_nonceToken()
        )
        lineaccount.save()
    return HttpResponse(status=200)

@handler.add(MessageEvent, message=TextMessage)
def DisConnect_LineAccount(event,token):
    lineaccount = LineAccount.objects.get(line_nonceToken = token)
    lineaccount.delete()
    return HttpResponse(status=200)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #if event.message.text == "ログイン":
        #return Connect_LineAccount()
    #elif event.message.text == "連係解除":
        #return DisConnect_LineAccount()

    reply = line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    return reply


def make_nonceToken():
    nonce_token = secrets.token_hex(16)
    return nonce_token

def push_message(userid, messages):
    pushurl = "{}/bot/message/push".format(LINEBOT_ENDPOINT)
    body = {
            'replyToken': userid,
            'messages': messages
    }
    req = urllib.request.Request(pushurl, json.dumps(body).encode(), HEADER)
