import os
import json

import asyncio
from slack_bolt.async_app import AsyncApp
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.aws_lambda.async_handler import AsyncSlackRequestHandler


import logging
logging.basicConfig(level=logging.DEBUG)

from dotenv import load_dotenv
load_dotenv()

SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# Initializes your app with your bot token and signing secret
# https://api.slack.com/authentication/verifying-requests-from-slack
app = AsyncApp(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

def get_block_message(provided_schedules:dict):
    message_md="*This is the message*"
    with open("block_kit.json",'r') as file:
        blocks = json.load(file)["blocks"]
        blocks[1]["text"]["text"]=message_md
        blocks[2]["elements"][0]["value"]=provided_schedules["tentative_schedule"]

        blocks[5]["text"]["text"]=provided_schedules["alternate_schedule_1"]
        blocks[5]["accessory"]["value"]=provided_schedules["alternate_schedule_1"]

        blocks[6]["text"]["text"]=provided_schedules["alternate_schedule_2"]
        blocks[6]["accessory"]["value"]=provided_schedules["alternate_schedule_2"]

        blocks[7]["text"]["text"]=provided_schedules["alternate_schedule_3"]
        blocks[7]["accessory"]["value"]=provided_schedules["alternate_schedule_3"]
    return json.dumps(blocks)

def get_view(private_metadata: dict, confirmation_message: str):
    with open('modal.json', 'r') as file:
        blocks = json.load(file)
        blocks["blocks"][2]["text"]["text"]=confirmation_message
        blocks["private_metadata"]=json.dumps(private_metadata)
    return json.dumps(blocks)

def get_shortcut(private_metadata: str):
    with open('shortcut.json', 'r') as file:
        blocks = json.load(file)
        blocks["private_metadata"]=json.dumps(private_metadata)
    return json.dumps(blocks)

async def respond_to_slack_within_3_seconds(ack):
    await ack()

async def handle_some_action(client, body, logger):
    try:
        logger.info(body)
        trigger_id=body["trigger_id"]
        private_metadata={
            "date":body["actions"][0]["value"],
            "message_ts":body["message"]["ts"],
            "user_id":body["container"]["channel_id"]
        }
        confirmation_message=f"I am scheduling my Windows upgrade on {body["actions"][0]["value"]}"
        await client.views_open(
            view=get_view(private_metadata, confirmation_message),
            trigger_id=trigger_id
        )
    except SlackApiError as e:
        logger.error(f"Failed to open modal: {e}")
app.action("confirm_date")(ack=respond_to_slack_within_3_seconds, lazy=[handle_some_action])

async def open_modal_reschedule(body, client, logger):
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

        await client.views_open(
            view=get_view(private_metadata, confirmation_message),
            trigger_id=trigger_id
        )
    except SlackApiError as e:
        logger.error(f"Failed to open modal: {e}")

reschedule_action_ids = [
    "confirm_reschedule_1",
    "confirm_reschedule_2",
    "confirm_reschedule_3"
]
for action_id in reschedule_action_ids:
    app.action(action_id)(ack=respond_to_slack_within_3_seconds, lazy=[open_modal_reschedule])

async def handle_view_submission_events(body, client, logger):
    try:
        logger.info(body)
        private_metadata=json.loads(body["view"]["private_metadata"])
        await client.chat_update(
            channel=private_metadata["user_id"],
            ts=private_metadata["message_ts"],
            text=f"You've confirmed your Windows upgrade for {private_metadata["date"]}"
        )
    except SlackApiError as e:
        logger.error(f"Failed to open modal: {e}")
app.view("confirmation_view")(ack=respond_to_slack_within_3_seconds, lazy=[handle_view_submission_events])

async def handle_global_shortcut(body, client, logger):
    try:
        await client.views_open(
            trigger_id=body["trigger_id"],
            view=get_shortcut("private_metadata")
        )
    except SlackApiError as e:
        logger.error(f"Failed to open modal: {e}")
app.shortcut("windows_update_callbackid")(ack=respond_to_slack_within_3_seconds, lazy=[handle_global_shortcut])


async def send_windows_message(email: str, schedules: dict[str:str]):
    try:
        response = await app.client.users_lookupByEmail(email=email)
        user_id = response["user"]["id"]
        await app.client.chat_postMessage(
            channel=user_id,
            blocks=get_block_message(schedules),
            text="Message from Endpoint Engineering"
        )
    except SlackApiError as e:
        print(f"Failed for {email}: {e.response['error']}")

async def message_multiple_users(emails: list[str], schedules:dict[str:str]):
    await asyncio.gather(*(send_windows_message(email.strip(), schedules) for email in emails))


async def handle_view_submission_events(ack, body, logger, view):
    await ack()
    logger.info(body)
    provided_emails=view["state"]["values"]["provided_emails"]["provided_emails-action"]["value"].split(",")

    provided_schedules={
        "tentative_schedule": view["state"]["values"]["tentative_schedule"]["tentative_schedule-action"]["value"],
        "alternate_schedule_1": view["state"]["values"]["alternate_schedule_1"]["alternate_schedule_1-action"]["value"],
        "alternate_schedule_2": view["state"]["values"]["alternate_schedule_2"]["alternate_schedule_2-action"]["value"],
        "alternate_schedule_3": view["state"]["values"]["alternate_schedule_3"]["alternate_schedule_3-action"]["value"]
    }

    await message_multiple_users(provided_emails, provided_schedules)

app.view("windows_update_modal_view")(ack=respond_to_slack_within_3_seconds, lazy=[handle_view_submission_events])

async def handler(event, context):
    return await AsyncSlackRequestHandler(app).handle(event, context)