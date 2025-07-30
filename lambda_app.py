import os
import json

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_sdk.errors import SlackApiError

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

def get_view(private_metadata: dict, confirmation_message: str):
    with open('modal.json', 'r') as file:
        blocks = json.load(file)
        blocks["blocks"][2]["text"]["text"]=confirmation_message
        blocks["private_metadata"]=json.dumps(private_metadata)
    return json.dumps(blocks)

app.client.chat_postMessage(
    channel=CHANNEL_ID,
    blocks=get_block_message(),
    text="Message from Endpoint Engineering"
)

@app.action("confirm_date")
def handle_some_action(ack, client, body, logger):
    ack()
    logger.info(body)
    trigger_id=body["trigger_id"]
    private_metadata={
        "date":body["actions"][0]["value"],
        "message_ts":body["message"]["ts"],
        "user_id":body["container"]["channel_id"]
    }
    confirmation_message=f"I am scheduling my Windows upgrade on {body["actions"][0]["value"]}"
    client.views_open(
        view=get_view(private_metadata, confirmation_message),
        trigger_id=trigger_id
    )
"""
@app.action("confirm_reschedule_1")
def handle_some_action(ack, client, body, logger):
    ack()
    logger.info(body)
    trigger_id=body["trigger_id"]
    private_metadata={
        "date":body["actions"][0]["value"],
        "message_ts":body["message"]["ts"],
        "user_id":body["container"]["channel_id"]
    }
    confirmation_message=f"I am scheduling my Windows upgrade on {body["actions"][0]["value"]}"
    client.views_open(
        view=get_view(private_metadata, confirmation_message),
        trigger_id=trigger_id
    )

@app.action("confirm_reschedule_2")
def handle_some_action(ack, client, body, logger):
    ack()
    logger.info(body)
    trigger_id=body["trigger_id"]
    private_metadata={
        "date":body["actions"][0]["value"],
        "message_ts":body["message"]["ts"],
        "user_id":body["container"]["channel_id"]
    }
    confirmation_message=f"I am scheduling my Windows upgrade on {body["actions"][0]["value"]}"
    client.views_open(
        view=get_view(private_metadata, confirmation_message),
        trigger_id=trigger_id
    )

@app.action("confirm_reschedule_3")
def handle_some_action(ack, client, body, logger):
    ack()
    logger.info(body)
    trigger_id=body["trigger_id"]
    private_metadata={
        "date":body["actions"][0]["value"],
        "message_ts":body["message"]["ts"],
        "user_id":body["container"]["channel_id"]
    }
    confirmation_message=f"I am scheduling my Windows upgrade on {body["actions"][0]["value"]}"
    client.views_open(
        view=get_view(private_metadata, confirmation_message),
        trigger_id=trigger_id
    )
  """  

def open_modal_reschedule_3(body, client, logger):
    try:
        logger.info(body)

        trigger_id = body["trigger_id"]
        selected_date = body["actions"][0]["value"]

        private_metadata = {
            "date": selected_date,
            "message_ts": body["message"]["ts"],
            "user_id": body["container"]["channel_id"]
        }

        confirmation_message = f"I am scheduling my Windows upgrade on {selected_date}"

        client.views_open(
            view=get_view(private_metadata, confirmation_message),
            trigger_id=trigger_id
        )
    except Exception as e:
        logger.error(f"Error opening modal for reschedule_3: {e}")

def respond_to_slack_within_3_seconds(ack):
    ack()

reschedule_action_ids = [
    "confirm_reschedule_1",
    "confirm_reschedule_2",
    "confirm_reschedule_3"
]

for action_id in reschedule_action_ids:
    app.action(action_id)(ack=respond_to_slack_within_3_seconds, lazy=[open_modal_reschedule_3])

@app.view("confirmation_view")
def handle_view_submission_events(ack, body, client, logger):
    ack()
    logger.info(body)
    private_metadata=json.loads(body["view"]["private_metadata"])
    client.chat_update(
        channel=private_metadata["user_id"],
        ts=private_metadata["message_ts"],
        text=f"You've confirmed your Windows upgrade for {private_metadata["date"]}"
    )

# Lambda adapter
# handler = SlackRequestHandler(app)

# AWS Lambda entrypoint
def lambda_handler(event, context):
    handler = SlackRequestHandler(app)
    return handler.handle(event, context)