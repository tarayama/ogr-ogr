from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError,)
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render
import requests
import json
import traceback
import os
try:
    import Linebot.environment_valiable
except:
    pass

def Errorlog_post_to_Slack(text):
    SlackURL = os.environ['Slack_Webhook_URL']
    headers = { 'Content-type': 'application/json' }
    response = requests.post(
        SlackURL,
        headers = headers,
        data = json.dumps({
            'text': text,
            'username': 'OGR^2 エラー通知',
            'icon_emoji': ':jack_o_lantern:',
        })
    )
    return response.status_code

#実行環境でエラーが起きたらSlackにエラー内容を送信する
@requires_csrf_token
def my_customized_server_error(request, template_name='400.html'):
    print(traceback.format_exc())
    text = '\n'.join([
        f'Request uri: {request.build_absolute_uri()}',
        traceback.format_exc()
    ])
    status_code = Errorlog_post_to_Slack(text)
    print(status_code)
    err_title = "エラーコード : {}".format(status_code)
    err_subt = "{}にてエラーが発生しました".format(request.build_absolute_uri())
    err_msg = "URL・内容を確認の上、再度時間を空けてお試しください"
    context = {
        'err_title' : err_title,
        'err_subt' : err_subt,
        'err_msg' : err_msg
    }
    return render(request, 'ogr/error.html', context)
