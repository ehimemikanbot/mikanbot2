from flask import Flask, request, abort
import requests
from bs4 import BeautifulSoup
import lxml.html
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    word = event.message.text
    url = "https://www.weblio.jp/content/" + word
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'}
    r = requests.get(url, headers=headers)
    html = r.text
    bs = BeautifulSoup(html, 'lxml')
    try:
        meanings = bs.select_one("#cont > div:nth-child(6) > div > div.NetDicBody").text
    except AttributeError:
        meanings = "三省堂 大辞林 第三版には存在しません"

    #実用語も検索
    try:
        meanings2=bs.select_one("#cont > div.kijiWrp > div > div").text
    except AttributeError:
        meanings2 = "実用日本語表現辞典には存在しません"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=word + '\n(三省堂 大辞林 第三版)' + meanings.lstrip() + '\n\n(実用日本語表現辞典)' + meanings2.lstrip()))



if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
    