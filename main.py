#質問形式botの方

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
    TemplateSendMessage,ButtonsTemplate,URIAction,PostbackAction,PostbackTemplateAction #こ↑こ↓が追加分
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# def make_button_template():
#     message_template = TemplateSendMessage(
#         alt_text="にゃーん",
#         template=ButtonsTemplate(
#             text="どれか選んでください",
#             title="タイトル",
#             actions=[
#                 PostbackTemplateAction(
#                     label='ON',
#                     data='is_show=1'
#                 ),
#                 PostbackTemplateAction(
#                     label='OFF',
#                     data='is_show=0'
#                 )
#             ]
#         )
#     )
#     return message_template


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
def handle_image_message(event):
    # messages = make_button_template()
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     messages
    # )
# def handle_message(event):

    #オウム返しにいったんもどし
    gettext=event.message.text
    if gettext in ['天気','てんき']
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='明日は真夏日です'))
    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))



# @handler.add(PostbackEvent)
# def on_postback(event):
#     reply_token = event.reply_token
#     user_id = event.source.user_id
#     postback_msg = event.postback.data

#     if postback_msg == 'is_show=1':
#         line_bot_api.push_message(
#             to=user_id,
#             messages=TextSendMessage(text='is_showオプションは1だよ！')
#         )
#     elif postback_msg == 'is_show=0':
#         line_bot_api.push_message(
#             to=user_id,
#             messages=TextSendMessage(text='is_showオプションは0だよ！')
#         )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
    