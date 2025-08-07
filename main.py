import os
import json
import datetime
from zoneinfo import ZoneInfo

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

app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

def get_todays_date() -> str:
    """Returns today's date in the format %Y-%m-%d %I:%M:%S %p %Z."""
    # Get the current datetime object
    now = datetime.datetime.now()
    # Convert to Pacific Time (Los Angeles)
    pacific_timezone = ZoneInfo("America/Los_Angeles") 
    now_aware = now.astimezone(pacific_timezone)
    formatted_datetime = now_aware.strftime("%Y-%m-%d")
    return formatted_datetime

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

def get_shortcut(private_metadata: str):
    todays_date = get_todays_date()
    with open('shortcut.json', 'r') as file:
        blocks = json.load(file)
        blocks["private_metadata"]=json.dumps(private_metadata)
    return json.dumps(blocks)

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

@app.shortcut("windows_update_callbackid")
def handle_global_shortcut(ack, body, client, logger):
    ack() 
    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=get_shortcut("private_metadata")
        )
    except Exception as e:
        logger.error(f"Failed to open modal: {e}")

@app.view("windows_update_modal_view")
def handle_view_submission_events(ack, body, logger, view):
    ack()
    logger.info(body)
    provided_emails=view["state"]["values"]["provided_emails"]["provided_emails-action"]["value"]
    tentative_schedule=view["state"]["values"]["tentative_schedule"]["tentative_schedule-action"]["value"]
    alternate_schedule_1=view["state"]["values"]["alternate_schedule_1"]["alternate_schedule_1-action"]["value"]
    alternate_schedule_2=view["state"]["values"]["alternate_schedule_2"]["alternate_schedule_2-action"]["value"]
    alternate_schedule_3=view["state"]["values"]["alternate_schedule_3"]["alternate_schedule_3-action"]["value"]

    app.client.chat_postMessage(
        channel=CHANNEL_ID,
        #blocks=get_block_message(),
        text=f"{alternate_schedule_1}\n{tentative_schedule}\n{alternate_schedule_2}\n{alternate_schedule_3}"
    )
        

if __name__ == "__main__":      
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
