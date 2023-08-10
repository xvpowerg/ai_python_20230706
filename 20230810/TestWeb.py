"""
from flask import Flask   
app = Flask(__name__) 
@app.route("/")           
def home():               
    return "<h1>hello world</h1>"   
app.run() 
"""
"""
from itsdangerous import exc
from flask import Flask,request
import json
from linebot import  LineBotApi,WebhookHandler
from linebot.models import TextSendMessage
app=Flask(__name__)
@app.route('/',methods=['POST'])
def linebot():
  body=request.get_data(as_text=True)
  json_data=json.loads(body)
  print('json_data:\n',json_data)
  try:
    line_bot_api=LineBotApi('')
    handler=WebhookHandler('')
    signature=request.headers['X-Line-Signature']
    handler.handle(body,signature)
    tk=json_data['events'][0]['replyToken']
    msg=json_data['events'][0]['message']['text']
    print('json_Data:\n')
    print(json_data)
    text_message=TextSendMessage(text=msg)
    line_bot_api.reply_message(tk,text_message)
  except:
    print('error')
  return 'ok'
app.run()  
"""
"""
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests, json, time
app = Flask(__name__)

access_token=''
channel_secret=''
@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)    
    try:
        line_bot_api = LineBotApi(access_token)               
        handler = WebhookHandler(channel_secret)              
        signature = request.headers['X-Line-Signature']        
        handler.handle(body, signature)                        
        json_data = json.loads(body)                           
        reply_token = json_data['events'][0]['replyToken']    
        user_id = json_data['events'][0]['source']['userId']  
        print(json_data)                                      
        if 'message' in json_data['events'][0]:                
            if json_data['events'][0]['message']['type'] == 'text':   
                text = json_data['events'][0]['message']['text']      
                if text == '雷達回波圖' or text == '雷達回波':           
                    reply_image(f'https://cwbopendata.s3.ap-northeast-1.amazonaws.com/MSC/O-A0058-003.png?{time.time_ns()}', reply_token, access_token)
    except:
        print('error')                       
    return 'OK'
def reply_image(msg, rk, token):
    headers = {'Authorization':f'Bearer {token}','Content-Type':'application/json'}    
    body = {
    'replyToken':rk,
    'messages':[{
          'type': 'image',
          'originalContentUrl': msg,
          'previewImageUrl': msg
        }]
    }
    req = requests.request('POST', 'https://api.line.me/v2/bot/message/reply', headers=headers,data=json.dumps(body).encode('utf-8'))
    print(req.text)         
app.run()
"""
from  flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests, json, time
import openai
app = Flask(__name__)

access_token=''
channel_secret=''
openAiKey=''
@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        line_bot_api = LineBotApi(access_token)
        handler = WebhookHandler(channel_secret)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']
        msg = json_data['events'][0]['message']['text']
        ai_msg = msg[:6].lower()
        reply_msg = ''
        # 取出文字的前五個字元是 hi ai:
        if ai_msg == 'hi ai:':
            print("OpenAI!!!")
            openai.api_key = openAiKey
            # 將第六個字元之後的訊息發送給 OpenAI
            response = openai.Completion.create(
                model='text-davinci-003',
                prompt=msg[6:],
                max_tokens=256,
                temperature=0.5,
                )
            reply_msg = response["choices"][0]["text"].replace('\n','')
        else:
            reply_msg = msg
        text_message = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(tk,text_message)
    except Exception as err:
        print('error:',err)
    return 'OK'
if __name__ == "__main__": 
    app.run()
