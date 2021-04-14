from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError,)
import requests
import json
import traceback

def Errorlog_post_to_Slack(request):
    SlackURL = "https://hooks.slack.com/service/T018AUPM5RU/B01U2573P7G/bCC7RDlJoU8P1ycH0DiSTz7m"
    headers = { 'Content-type': 'application/json' }
    response = requests.post(
        SlackURL,
        headers = headers,
        data = json.dumps({
            'text': '\n'.join([
                f'Request uri: {request.build_absolute_uri()}',
                traceback.format_exc(),
            ]),
            'username': 'OGR^2 エラー通知',
            'icon_emoji': ':jack_o_lantern:',
        })
    )
    return response.status_code
