from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError,)
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render
import requests
import json
import traceback
import sys
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
def my_customized_server400_error(request, template_name='400.html'):
    errcode = 400
    uri = request.build_absolute_uri()
    print(traceback.format_exc())
    text = '\n'.join([
        f'Request uri: {uri}',
        traceback.format_exc()
    ])
    status_code = Errorlog_post_to_Slack(text)
    print(status_code)
    type_, value, traceback_ = sys.exc_info()
    err_title = "エラーコード : {}".format(errcode)
    err_subt = value
    err_msg = "URL・内容を確認の上、再度時間を空けてお試しください"
    context = {
        'err_title' : err_title,
        'err_subt' : err_subt,
        'err_msg' : err_msg
    }
    return render(request, 'ogr/error.html', context)

@requires_csrf_token
def my_customized_server403_error(request, template_name='403.html'):
    errcode = 403
    uri = request.build_absolute_uri()
    print(traceback.format_exc())
    text = '\n'.join([
        f'Request uri: {uri}',
        traceback.format_exc()
    ])
    status_code = Errorlog_post_to_Slack(text)
    print(status_code)
    type_, value, traceback_ = sys.exc_info()
    err_title = "エラーコード : {}".format(errcode)
    err_subt = value
    err_msg = "URL・内容を確認の上、再度時間を空けてお試しください"
    context = {
        'err_title' : err_title,
        'err_subt' : err_subt,
        'err_msg' : err_msg
    }
    return render(request, 'ogr/error.html', context)

@requires_csrf_token
def my_customized_server404_error(request, template_name='404.html'):
    errcode= 404
    uri = request.build_absolute_uri()
    print(traceback.format_exc())
    text = '\n'.join([
        f'Request uri: {uri}',
        traceback.format_exc()
    ])
    status_code = Errorlog_post_to_Slack(text)
    print(status_code)
    type_, value, traceback_ = sys.exc_info()
    err_title = "エラーコード : {}".format(errcode)
    err_subt = value
    err_msg = "URL・内容を確認の上、再度時間を空けてお試しください"
    context = {
        'err_title' : err_title,
        'err_subt' : err_subt,
        'err_msg' : err_msg
    }
    return render(request, 'ogr/error.html', context)

@requires_csrf_token
def my_customized_server500_error(request, template_name='500.html'):
    errcode = 500
    uri = request.build_absolute_uri()
    print(traceback.format_exc())
    text = '\n'.join([
        f'Request uri: {uri}',
        traceback.format_exc()
    ])
    status_code = Errorlog_post_to_Slack(text)
    print(status_code)
    type_, value, traceback_ = sys.exc_info()
    err_title = "エラーコード : {}".format(errcode)
    err_subt = value
    err_msg = "URL・内容を確認の上、再度時間を空けてお試しください"
    context = {
        'err_title' : err_title,
        'err_subt' : err_subt,
        'err_msg' : err_msg
    }
    return render(request, 'ogr/error.html', context)

