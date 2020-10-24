from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .message import *
# Create your views here.
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        request = json.loads(request.body.decode('utf-8'))
        events = request['events']
        for event in events:
            message = event['message']
            reply_token = event['replyToken']
            line_message = LineMessage()
            line_message.create_message(message['text'])
            line_message.reply(reply_token)
        return HttpResponse("ok")
