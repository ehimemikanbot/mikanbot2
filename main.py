from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,QuickReplyButton, MessageAction, QuickReply,
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

lesson = {
    '月曜日の時間割':'月曜日は\n1:こくご\n2:たいいく\n3:さんすう\nです。',
    '火曜日の時間割':'火曜日は\n1~2:りかじっけん\n3:こくご\nです。',
    '水曜日の時間割':'水曜日は\n1:さんすう\n2:おんがく\n3:せいかつ\nです。',
    '木曜日の時間割':'木曜日は\n1:たいいく\n2:かていか\n3:りか\nです。',
    '金曜日の時間割':'金曜日は\n1:さんすう\n2:こくご\n3:がっかつ\nです。'
}

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
    if event.message.text=='時間割を教えて':
        day_list=["月","火", "水", "木", "金"]
        items=[QuickReplyButton(action=MessageAction(label=f"{day}",text=f"{day}曜日の時間割")) for day in day_list]
        messages=TextSendMessage(text="何曜日の時間割ですか？",quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token,messages=messages)
    elif event.message.text in lesson:
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=lesson[event.message.text])
        )
    '''
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=re_text(event.message.text))
    )
    '''

# 送信されたメッセージから返信内容を設定する
'''
def re_text(gettext):
    if gettext=='1':
        settext='1ですね。'
    elif gettext=='2':
        settext='2ですね。'
    else:
        settext='そのたですね。'
    return settext
'''

# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
