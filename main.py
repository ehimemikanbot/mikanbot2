from flask import Flask, request, abort
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

#herokuへのデプロイが成功したかどうかを確認するためのコード
@app.route("/")
def hello_world():
    return "hello world!"

#LINE DevelopersのWebhookにURLを指定してWebhookからURLにイベントが送られるようにする
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.headers['X-Line-Signature']

    # get request body as textz
    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    # 署名を検証し、問題なければhandleに定義されている関数を呼ぶ
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#以下でWebhookから送られてきたイベントをどのように処理するかを記述する
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=re_text(event.message.text))
    )

# 送信されたメッセージから返信内容を設定する
def re_text(gettext):
    if gettext=='1':
        settext='1ですね。'
    elif gettext=='2':
        settext='2ですね。'
    else:
        settext='そのたですね。'
    return settext

# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
