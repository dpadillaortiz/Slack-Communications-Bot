import os
import json

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_sdk.errors import SlackApiError

import logging
logging.basicConfig(level=logging.DEBUG)

from dotenv import load_dotenv
load_dotenv()

SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# Initializes your app with your bot token and signing secret
# https://api.slack.com/authentication/verifying-requests-from-slack
app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET,
    process_before_response=True
)

def get_block_message(provided_schedules:dict):
    message_md=f'''
    Hi Workmate :wave:\n
    To keep your Workday-managed laptop secure and up-to-date, we're getting it ready for an upgrade to Windows 11 24H2. 
    We have tentatively scheduled yours for the week of {provided_schedules["tentative_schedule"]}.\n
    You can approve this time or choose a different week below. If you don't make a selection, your upgrade will proceed during this assigned week.\n
    *What to Expect:*
    - The upgrade will download in the background with no interruption to your work.
    - You'll receive a prompt to restart your device once the download is complete.
    - The final installation takes about 45 minutes after you restart, and your device will be unavailable during this time.
    - *Heads-up:* If you don't restart within 7 days of the prompt, your device will restart automatically to complete the upgrade.
    '''
    with open("block_kit.json",'r') as file:
        blocks = json.load(file)["blocks"]
        blocks[1]["text"]["text"]=message_md
        blocks[2]["elements"][0]["value"]=provided_schedules["tentative_schedule"]

        blocks[5]["text"]["text"]=f"Upgrade the week of *{provided_schedules['alternate_schedule_1']}*"
        blocks[5]["accessory"]["value"]=provided_schedules["alternate_schedule_1"]

        blocks[6]["text"]["text"]=f"Upgrade the week of *{provided_schedules['alternate_schedule_2']}*"
        blocks[6]["accessory"]["value"]=provided_schedules["alternate_schedule_2"]

        blocks[7]["text"]["text"]=f"Upgrade the week of *{provided_schedules['alternate_schedule_3']}*"
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

def respond_to_slack_within_3_seconds(ack):
    ack()

def handle_some_action(client, body, logger):
    try:
        logger.info(body)
        trigger_id=body["trigger_id"]
        private_metadata={
            "date":body["actions"][0]["value"],
            "message_ts":body["message"]["ts"],
            "user_id":body["container"]["channel_id"]
        }
        confirmation_message=f':spiral_calendar_pad: I am scheduling my Windows upgrade on *{body["actions"][0]["value"]}*.'
        client.views_open(
            view=get_view(private_metadata, confirmation_message),
            trigger_id=trigger_id
        )
    except SlackApiError as e:
        logger.info(body)
        logger.error(f"Failed to open modal: {e}")
app.action("confirm_date")(ack=respond_to_slack_within_3_seconds, lazy=[handle_some_action])

def open_modal_reschedule(body, client, logger):
    try:
        logger.info(body)

        trigger_id = body["trigger_id"]
        selected_date = body["actions"][0]["value"]

        private_metadata = {
            "date": selected_date,
            "message_ts": body["message"]["ts"],
            "user_id": body["container"]["channel_id"]
        }

        confirmation_message = f"I am scheduling my Windows upgrade on *{selected_date}*"

        client.views_open(
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

def handle_view_submission_events(body, client, logger):
    try:
        logger.info(body)
        private_metadata=json.loads(body["view"]["private_metadata"])
        client.chat_update(
            channel=private_metadata["user_id"],
            ts=private_metadata["message_ts"],
            text=f"You have selected the week of {private_metadata['date']} for your Windows 11 24H2 upgrade.\nClick `Confirm` to finalize this schedule."
        )
    except SlackApiError as e:
        logger.error(f"Failed to open modal: {e}")
app.view("confirmation_view")(ack=respond_to_slack_within_3_seconds, lazy=[handle_view_submission_events])

def handle_global_shortcut(body, client, logger):
    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=get_shortcut("private_metadata")
        )
    except SlackApiError as e:
        logger.error(f"Failed to open modal: {e}")
app.shortcut("windows_update_callbackid")(ack=respond_to_slack_within_3_seconds, lazy=[handle_global_shortcut])

def send_windows_message(client, email: str, schedules: dict[str:str]):
    try:
        response = app.client.users_lookupByEmail(email=email)
        user_id = response["user"]["id"]
        client.chat_postMessage(
            channel=user_id,
            blocks=get_block_message(schedules),
            text="Message from Endpoint Engineering"
        )
    except SlackApiError as e:
        print(f"Failed for {email}: {e.response['error']}")

def message_multiple_users(client, emails: list[str], schedules:dict[str:str]):
    for email in emails: send_windows_message(client, email.strip(), schedules) 

def handle_shortcut_submission_events(ack, body, client, logger, view):
    ack()
    logger.info(body)
    provided_emails=view["state"]["values"]["provided_emails"]["provided_emails-action"]["value"].split(",")
    provided_schedules={
        "tentative_schedule": view["state"]["values"]["tentative_schedule"]["tentative_schedule-action"]["value"],
        "alternate_schedule_1": view["state"]["values"]["alternate_schedule_1"]["alternate_schedule_1-action"]["value"],
        "alternate_schedule_2": view["state"]["values"]["alternate_schedule_2"]["alternate_schedule_2-action"]["value"],
        "alternate_schedule_3": view["state"]["values"]["alternate_schedule_3"]["alternate_schedule_3-action"]["value"]
    }
    message_multiple_users(client, provided_emails, provided_schedules)

app.view("windows_update_modal_view")(ack=respond_to_slack_within_3_seconds, lazy=[handle_shortcut_submission_events])

# AWS Lambda entrypoint
def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)