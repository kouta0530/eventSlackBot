import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from models import PosDB
from memory_profiler import profile

# Initialize a Flask app to host the events adapter
app = Flask(__name__)


#ここローカルでの実験用
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path,encoding="utf-8_sig")
#本番はherokuの環境変数

# Create an events adapter and register it to an endpoint in the slack app for event injestion.
slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))



from flask import request,Response
import json

@app.route("/",methods = ["POST"])
def test():
    data = request.data.decode("utf-8")
    data = json.loads(data)
    if "challenge" in data:
        token = str(data['challenge'])
        return Response(token, mimetype='text/plane')
    return 0



# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
"""
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
"""

@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]

    if(message.get("text") != None):
        text = message.get("text")
        from plugin import wordGet
        words = wordGet.mecab(text)

        """
        for word in words:
            model.setcursor()
            model.command("insert into words values(word);")
        """
    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get("subtype") is None and "hi" in message.get('text'):
        channel = message["channel"]
        message = "Hello <@%s>! :tada:" % message["user"]
        return slack_web_client.chat_postMessage(channel=channel, text=message)
    if message.get("subtype") is None and "天気" in message.get('text'):
        channel = message["channel"]
        message = "今日は...わからない"
        return slack_web_client.chat_postMessage(channel=channel, text=message)
    if message.get("subtype") is None and "ニュース" in message.get('text'):
        channel = message["channel"]
        from plugin import search
        message = search.get_news()
        return slack_web_client.chat_postMessage(channel=channel, text=message)

        


@slack_events_adapter.on("reaction_added")
def bookMark(event_data):
    item = event_data["event"]["item"]    
    channel = item["channel"]

    return slack_web_client.chat_postMessage(channel=channel,text="hello")



if __name__ == "__main__":
    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())
    # Run our app on our externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(port = 80)