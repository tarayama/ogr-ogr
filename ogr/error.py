from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError,)
from django.views.decorators.csrf import requires_csrf_token
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
def my_customized_server400_error(request, template_name='400.html'):
    print(traceback.format_exc())
    text = '\n'.join([
        f'Request uri: {request.build_absolute_uri()}',
        traceback.format_exc()
    ])
    status_code = Errorlog_post_to_Slack(text)
    print(status_code)
    return HttpResponseBadRequest('<h1>Bad Request (400)</h1><p>slack response code = {}</p>'.format(status_code))

@requires_csrf_token
def my_customized_server403_error(request, template_name='403.html'):
    print(traceback.format_exc())
    text = '\n'.join([
        f'Request uri: {request.build_absolute_uri()}',
        traceback.format_exc()
    ])
    status_code = Errorlog_post_to_Slack(text)
    print(status_code)
    return HttpResponseForbidden('<h1>Permissions Denied (403)</h1><p>slack response code = {}</p>'.format(status_code))

@requires_csrf_token
def my_customized_server404_error(request, template_name='404.html'):
    print(traceback.format_exc())
    text = '\n'.join([
        f'Request uri: {request.build_absolute_uri()}',
        traceback.format_exc()
    ])
    status_code = Errorlog_post_to_Slack(text)
    print(status_code)
    return HttpResponseNotFound('<h1>Page Not Found (404)</h1><p>slack response code = {}</p>'.format(status_code))

@requires_csrf_token
def my_customized_server500_error(request, template_name='500.html'):
    print(traceback.format_exc())
    text = '\n'.join([
        f'Request uri: {request.build_absolute_uri()}',
        traceback.format_exc()
    ])
    status_code = Errorlog_post_to_Slack(text)
    print(status_code)
    return HttpResponseServerError('<h1>Server Error (500)</h1><p>slack response code = {}</p>'.format(status_code))
