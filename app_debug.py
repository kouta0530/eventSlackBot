import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from PosDB import PosDB
from plugin import search
from plugin import wordGet

# Initialize a Flask app to host the events adapter
app = Flask(__name__)

#ここローカルでの実験用
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path,encoding="utf-8_sig")
#本番はherokuの環境変数


from flask import request,Response
import json
@app.route("/",methods = ["POST"])
def test():
    data = request.data.decode("utf-8")
    data = json.loads(data)

    if "challenge" in data:
        token = token = str(data['challenge'])
        return Response(token, mimetype='text/plane')
    return 0

# Create an events adapter and register it to an endpoint in the slack app for event injestion.
slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))



host = os.environ.get("HOST")
dbname = os.environ.get("DBNAME")
users = os.environ.get("USER")
password = os.environ.get("PASS")
port = int(os.environ.get("PORT"))
url = os.environ.get("DB_URL")

#作ったテーブル：create table news(id serial primary key, news_address text, users_id varchar(20), tag varchar(100));
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    

    if request.headers.get("X-Slack-Retry-Num"):
        return {"statusCode":200,"body":""}

    if message.get("bot_id") is None:
        channel = message["channel"]
        """
        wordlist = wordGet.mecab(message.get('text'))
        pos_db = PosDB(host,dbname,users,password,port,url)
        pos_db.set_cursor()
        for i in wordlist:
            sql_words = "insert into words (word) select '%s' where not exists (select * from words where word = '%s')" % (i,i)
            pos_db.insert_command(sql_words)
        pos_db.close()
        """
        if message.get('text') == "おこのみ":
            sql_words = "select word from words"
            pos_db = PosDB(host,dbname,users,password,port,url)
            pos_db.set_cursor()
            result = pos_db.select_command(sql_words)
            pos_db.close()

            menthion = [i["word"] for i in result]
            newsList = search.get_news_list()
            
            for i in newsList:
                text = search.filter_search(i)
                word = wordGet.mecab(text)
                if search.compare_words(menthion,word):
                    slack_web_client.chat_postMessage(channel=channel,text="好みの記事を見つけたよ")
                    return slack_web_client.chat_postMessage(channel=channel,text = i)

            return slack_web_client.chat_postMessage(channel=channel,text="ありませんでした")


        if message.get('text') == "ニュース" and message.get("thread_ts") is None:
            botmessage = search.get_news()
            return slack_web_client.chat_postMessage(channel=channel, text=botmessage)
            


        if message.get('text') is not None and message.get('text').startswith('ブックマーク') and message.get("thread_ts") is None:
            user = message["user"]
            pos_db = PosDB(host,dbname,users,password,port,url)
            pos_db.set_cursor()
            if message.get('text') != 'ブックマーク' and (message.get('text').find(' ') or message.get('text').find('　')):
                sql_news = "select * from news where tag = '%s'" % message.get('text').replace('　','')[6:]
                result = pos_db.select_command(sql_news)
                pos_db.close()
                if len(result)==0:
                    botmessage = "タグ:'%s' のタグはまだ付けられてないよ" % message.get('text').replace('　','')[6:]
                    return slack_web_client.chat_postMessage(channel=channel, text=botmessage)
                else:
                    for value in result:
                        slack_web_client.chat_postMessage(channel=channel, text=value['news_address'])
                    botmessage = "タグ:%s のリンク一覧だよ" % message.get('text').replace('　','')[6:]
                    return slack_web_client.chat_postMessage(channel=channel, text=botmessage)
                    
            else:
                sql_news = "SELECT * FROM news where users_id = '%s'" % user
                result = pos_db.select_command(sql_news)
                pos_db.close()
                if len(result)==0:
                    botmessage = "まだあなたが登録した記事はないよ"
                    return slack_web_client.chat_postMessage(channel=channel, text=botmessage)
                else:
                    for value in result:
                        slack_web_client.chat_postMessage(channel=channel, text=value['news_address'])
                    botmessage = "あなたがお気に入りにしている記事を取得したよ"
                    return slack_web_client.chat_postMessage(channel=channel, text=botmessage)
                    


        if message.get('text') is not None and message.get('text').startswith('おすすめ') and message.get("thread_ts") is None:
            user = message["user"]
            pos_db = PosDB("localhost", "slackbot", "postgres", "postgres", 5432,url)
            pos_db.set_cursor()
            sql_news = "SELECT * FROM news where not users_id = '%s'" % user
            result = pos_db.select_command(sql_news)
            pos_db.close()
            if len(result)==0:
                botmessage = "まだ他の人はお気に入りにしてないなあ"
                return slack_web_client.chat_postMessage(channel=channel, text=botmessage)
            else:
                for value in result:
                    slack_web_client.chat_postMessage(channel=channel, text=value['news_address'])
                botmessage = "みんなはこんな記事をお気に入りしてるよ"
                return slack_web_client.chat_postMessage(channel=channel, text=botmessage)
                
            
            
        if message.get("thread_ts") is not None: #botの投稿以外かつスレッドの投稿のみに反応
            thread_ts = message["thread_ts"]
            history_top = slack_web_client.conversations_replies(ts= thread_ts ,channel = channel)['messages'][0]
            #history_type = history_top['blocks'][0]['elements'][0]['elements'][0]['type']
            '''
            if "取得テスト" in message.get('text'):
                #slack_web_client.chat_postMessage(channel=channel, text=event_data)
                pos_db = PosDB("localhost", "slackbot", "postgres", "postgres", 5432)
                pos_db.set_cursor()
                result = pos_db.select_command("SELECT * FROM test")
                pos_db.close()
                for value in result:
                    slack_web_client.chat_postMessage(thread_ts=thread_ts, channel=channel, text=value['url'])
                botmessage = "取得したよ"
                slack_web_client.chat_postMessage(thread_ts=thread_ts, channel=channel, text=botmessage)
                return 0
            '''
            if message.get('text').startswith('ブックマーク') and history_top['text'].startswith('<http'):
                user = message["user"]
                link = history_top['text']
                sql_news = "insert into news (news_address, users_id) select '%s','%s' where not exists (select * from news where news_address = '%s' and users_id = '%s')" %(link, user, link, user)
                pos_db = PosDB(host,dbname,users,password,port,url)
                pos_db.set_cursor()
                pos_db.insert_command(sql_news)
                if message.get('text') != 'ブックマーク' and (message.get('text').find(' ') or message.get('text').find('　')):
                    sql_news = "update news set tag='%s' where news_address='%s' and users_id='%s'" %(message.get('text').replace('　','')[6:], link, user)
                    pos_db.insert_command(sql_news)
                    pos_db.close()
                    botmessage = "タグをつけたよ"
                    return slack_web_client.chat_postMessage(thread_ts=thread_ts, channel=channel, text=botmessage)
                else:
                    pos_db.close()
                    botmessage = "お気に入りにしたよ"
                    return slack_web_client.chat_postMessage(thread_ts=thread_ts, channel=channel, text=botmessage)
                    
            '''
            if "挿入テスト" in message.get('text'):
                sql = "insert into test (url,tag) values ('%s','%s')" % (message.get('text'), message.get('text'))
                pos_db = PosDB("localhost", "slackbot", "postgres", "postgres", 5432)
                pos_db.set_cursor()
                pos_db.insert_command(sql)
                pos_db.close()
                botmessage = "挿入したよ"
                slack_web_client.chat_postMessage(thread_ts=thread_ts, channel=channel, text=botmessage)
                return 0
            if "テスト" in message.get('text'):
                slack_web_client.chat_postMessage(thread_ts = thread_ts ,channel=channel, text=message['text'])
                botmessage = slack_web_client.conversations_replies(ts= thread_ts ,channel = channel)
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                print(history_top)
                #slack_web_client.chat_postMessage(['attachments'][0]['title_link'] is not None)
                #slack_web_client.chat_postMessage(thread_ts = thread_ts ,channel=channel, text=botmessage['messages'][0]['blocks'][0]['elements'][0]['elements'][0]['type'])
                #slack_web_client.chat_postMessage(channel=channel, text=event_data)
                return 0
            '''
        

# Example reaction emoji echo
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    event = event_data["event"]
    #emoji = event["reaction"]
    channel = event["item"]["channel"]
    #eventitem = event["item"]
    #text = ":%s:" % emoji
    #if eventitem.get("bot_id") is None:
        #slack_web_client.chat_postMessage(channel=channel, text=text)
    slack_web_client.chat_postMessage(channel=channel, text=event_data)
    return 0

# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

if __name__ == "__main__":
    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())

    # Run our app on our externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host='0.0.0.0', port=80, debug=True)

