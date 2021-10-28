# send the msg in slack by using code
# import slack
# import os
# from pathlib import Path
# from dotenv import load_dotenv
#
#
# env_path = Path('.') / '.env'
# print(env_path)
#
# load_dotenv(dotenv_path = env_path)
#
# client = slack.WebClient(token = os.environ['SLACK_TOKEN'])
#
# client.chat_postMessage(channel= '#in_it_to_win_it', text = "HEllO, How may I help you?")

import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
from datetime import date

env_path = Path('.') / '.env'
print(env_path)

load_dotenv(dotenv_path = env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token = os.environ['SLACK_TOKEN'])
BOT_ID =client.api_call("auth.test")['user_id']

@slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get('event',{})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    EXAMPLE_COMMAND = ['HI','Hello', 'Hi', 'hi', 'hello']
    EXAMPLE_COMMAND1 = ['What is your name?', 'What is your work?']
    EXAMPLE_COMMAND2 = ['What is the date today?', 'what is the date today?', "today's date?", "Today's date?"]
    if user_id != BOT_ID:
        for i in range (len(EXAMPLE_COMMAND)):
            #EXAMPLE_COMMAND = EXAMPLE_COMMAND[i].lower()
            if text.startswith(tuple(EXAMPLE_COMMAND[i])):
                response = "Hello!! Welcome to the IT bot!! How may I help You?"
                client.chat_postMessage(channel = channel_id, text = response)
            elif text.startswith(tuple(EXAMPLE_COMMAND1)):
                response1 = "My name is IT_bot and my job is to take customer's feedback."
                client.chat_postMessage(channel = channel_id, text = response1)
            elif text.startswith(tuple(EXAMPLE_COMMAND2)):
                today1 = date.today()
                today = today1.strftime("%m/%d/%y")
                response2 = today
                client.chat_postMessage(channel = channel_id, text = response2)


if __name__ == '__main__':
    app.run(debug = True)