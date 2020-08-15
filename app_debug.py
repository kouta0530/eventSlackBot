import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from coinbot import CoinBot
from PosDB import PosDB

# Initialize a Flask app to host the events adapter
app = Flask(__name__)

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

def flip_coin(channel):
    #Craft the CoinBot, flip the coin and send the message to the channel
    # Create a new CoinBot
    coin_bot = CoinBot(channel)

    # Get the onboarding message payload
    message = coin_bot.get_message_payload()

    # Post the onboarding message in Slack
    slack_web_client.chat_postMessage(**message)

'''
# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("message")
def message(payload):
    #Parse the message event, and if the activation string is in the text,
    #simulate a coin flip and send the result.
    

    # Get the event data from the payload
    event = payload.get("event", {})

    # Get the text from the event that came through
    text = event.get("text")

    # Check and see if the activation phrase was in the text of the message.
    # If so, execute the code to flip a coin.
    if "hey sammy, flip a coin" in text.lower():
        # Since the activation phrase was met, get the channel ID that the event
        # was executed on
        channel_id = event.get("channel")

        # Execute the flip_coin function and send the results of
        # flipping a coin to the channel
        return flip_coin(channel_id)

'''
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    if message.get("bot_id") is None and message.get("thread_ts") is not None: #botの投稿以外かつスレッドの投稿のみに反応
        if "取得テスト" in message.get('text'):
            channel = message["channel"]
            botmessage = "取得したよ"
            slack_web_client.chat_postMessage(channel=channel, text=botmessage)
            #slack_web_client.chat_postMessage(channel=channel, text=event_data)
            pos_db = PosDB()
            pos_db.set_cursor()
            result = pos_db.command("SELECT * FROM test")
            slack_web_client.chat_postMessage(channel=channel, text=result[0][url])
            return 0
        if "ブックマーク" in message.get('text'):
            channel = message["channel"]
            thread_ts = message["thread_ts"]
            botmessage = "ブックマークしたよ"
            slack_web_client.chat_postMessage(thread_ts=thread_ts, channel=channel, text=botmessage)
            slack_web_client.chat_postMessage(channel=channel, text=event_data)
            return 0
        if "挿入テスト" in message.get('text'):
            channel = message["channel"]
            botmessage = "挿入したよ"
            sql = "insert into test (url,tag) values ('%s','%s')" % (message.get('text'), message.get('text'))
            #slack_web_client.chat_postMessage(channel=channel, text=event_data)
            pos_db = PosDB()
            pos_db.set_cursor()
            pos_db.command2(sql)
            slack_web_client.chat_postMessage(channel=channel, text=botmessage)
            return 0
        if "テスト" in message.get('text'):
            channel = message["channel"]
            thread_ts = message["thread_ts"]
            slack_web_client.chat_postMessage(thread_ts = thread_ts ,channel=channel, text=message['text'])
            botmessage = slack_web_client.conversations_replies(ts= thread_ts ,channel = channel)
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            print(botmessage)
            slack_web_client.chat_postMessage(thread_ts = thread_ts ,channel=channel, text=botmessage['messages'][0]['text'])
            return 0

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
    app.run(host='0.0.0.0', port=5000, debug=True)

