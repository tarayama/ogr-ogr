from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import urllib.request
import json


REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/reply"

ACCESSTOKEN = 'ZlxbDtTS3SfT9gZjOc8FKgZ+Kkgga9/7VUqfmkb0v3pGOqQFjUA2+A86EJma9riHF32eneBx3fgN+pwEPMRURsbrKOnhWRCo4glIaXfW1W005VUgSEXI7F3wbC0ueR77b0Axq8HgOV2BLZVLJqA9aQdB04t89/1O/w1cDnyilFU='   
HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + ACCESSTOKEN
}

class LineMessage():
    def __init__(self, messages):
        self.messages = messages

    def reply(self, reply_token):
        body = {
            'replyToken': reply_token,
            'messages': self.messages
        }
        print(body)
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)
    
def create_message(message):
        test_message = [
                    {
                        'type': 'text',
                        'text': message
                    }
                ]
        return test_message

