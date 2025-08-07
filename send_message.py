import os
import json

from slack_bolt import App
from slack_sdk.errors import SlackApiError


import asyncio
from slack_bolt.async_app import AsyncApp
from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_client import AsyncWebClient

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

async_app = AsyncApp(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)


def get_block_message():
    with open("block_kit.json",'r') as file:
        blocks = json.load(file)["blocks"]
    return json.dumps(blocks)


provided_emails=["hazrd510@gmail.com", "padillaortiz.daniel099@gmail.com"]

async def send_windows_message(email: str):
    try:
        user_id = await async_app.client.users_lookupByEmail(email=email)["user"]["id"]
        await async_app.client.chat_postMessage(
            channel=user_id,
            blocks=get_block_message(),
            text="Message from Endpoint Engineering"
        )
    except SlackApiError as e:
        print(f"Failed for {email}: {e.response['error']}")

async def message_multiple_users(emails: list[str]):
    await asyncio.gather(*(send_windows_message(email) for email in emails))
