import os
import json

from slack_bolt import App
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.socket_mode import SocketModeHandler

import logging
logging.basicConfig(level=logging.DEBUG)

from dotenv import load_dotenv
load_dotenv()

SLACK_APP_TOKEN= os.getenv("SLACK_APP_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID=os.getenv("CHANNEL_ID")

# Initializes your app with your bot token and signing secret
# https://api.slack.com/authentication/verifying-requests-from-slack
app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

def get_block_message():
    with open("block_kit.json",'r') as file:
        blocks = json.load(file)["blocks"]
    return json.dumps(blocks)

app.client.chat_postMessage(
    channel=CHANNEL_ID,
    blocks=get_block_message(),
    text="Message from Endpoint Engineering"
)