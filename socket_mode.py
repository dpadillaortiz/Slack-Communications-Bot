import os
import json
import ui_templates

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

# Top-level (runs once per cold start)
with open("modal.json", "r") as f:
    MODAL_TEMPLATE = json.load(f)

with open("block_kit.json", "r") as f:
    BLOCKS_TEMPLATE = json.load(f)

with open("shortcut.json", "r") as f:
    SHORTCUT_TEMPLATE = json.load(f)

# Initializes your app with your bot token and signing secret
# https://api.slack.com/authentication/verifying-requests-from-slack
app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET,
    process_before_response=True
)

def respond_to_slack_within_3_seconds(ack):
    ack()

def handle_confirm_tentative(client, body, logger):
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
            view=ui_templates.build_confirmation_modal(private_metadata, confirmation_message),
            #view=get_view(private_metadata, confirmation_message),
            trigger_id=trigger_id
        )
    except SlackApiError as e:
        logger.info(body)
        logger.error(f"Failed to open modal: {e}")
app.action("confirm_date")(ack=respond_to_slack_within_3_seconds, lazy=[handle_confirm_tentative])

def handle_alternative_choice(body, client, logger):
    try:
        logger.info(body)
        trigger_id = body["trigger_id"]
        selected_date = body["actions"][0]["value"]
        private_metadata = {
            "date": selected_date,
            "message_ts": body["message"]["ts"],
            "user_id": body["container"]["channel_id"]
        }
        confirmation_message = f":spiral_calendar_pad: I am scheduling my Windows upgrade on *{selected_date}*"
        client.views_open(
            # view=get_view(private_metadata, confirmation_message),
            view=ui_templates.build_confirmation_modal(private_metadata, confirmation_message),
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
    app.action(action_id)(ack=respond_to_slack_within_3_seconds, lazy=[handle_alternative_choice])

def handle_view_submission_events(body, client, logger):
    try:
        logger.info(body)
        private_metadata=json.loads(body["view"]["private_metadata"])
        client.chat_update(
            channel=private_metadata["user_id"],
            ts=private_metadata["message_ts"],
            text=f"You have selected the week of {private_metadata['date']} for your {private_metadata['windows_version']} upgrade."
        )
    except SlackApiError as e:
        logger.error(f"Failed to open modal: {e}")
app.view("confirmation_view")(ack=respond_to_slack_within_3_seconds, lazy=[handle_view_submission_events])

def handle_global_shortcut(body, client, logger):
    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            #view=get_shortcut("private_metadata")
            view=ui_templates.build_shortcut_modal("private_metadata")
        )
    except SlackApiError as e:
        logger.error(f"Failed to open modal: {e}")
app.shortcut("windows_update_callbackid")(ack=respond_to_slack_within_3_seconds, lazy=[handle_global_shortcut])

def send_windows_message(client, email: str, schedules: dict[str:str], windows_version:str):
    try:
        response = app.client.users_lookupByEmail(email=email)
        user_id = response["user"]["id"]
        client.chat_postMessage(
            channel=user_id,
            #blocks=get_block_message(schedules),
            blocks=ui_templates.build_blocks_message(schedules, windows_version),
            text="Message from Endpoint Engineering"
        )
    except SlackApiError as e:
        print(f"Failed for {email}: {e.response['error']}")

def message_multiple_users(client, emails: list[str], schedules:dict[str:str], windows_version:str):
    for email in emails: send_windows_message(client, email.strip(), schedules, windows_version) 


def handle_shortcut_submission_events(ack, body, client, logger, view):
    ack()
    logger.info(body)
    windows_version=view["state"]["values"]["windows_version"]["windows_version-action"]["value"]
    ui_templates.update_confirmation_template({"windows_version":windows_version})
    provided_emails=view["state"]["values"]["provided_emails"]["provided_emails-action"]["value"].split(",")
    provided_schedules={
        "windows_version":view["state"]["values"]["windows_version"]["windows_version-action"]["value"],
        "tentative_schedule": view["state"]["values"]["tentative_schedule"]["tentative_schedule-action"]["value"],
        "alternate_schedule_1": view["state"]["values"]["alternate_schedule_1"]["alternate_schedule_1-action"]["value"],
        "alternate_schedule_2": view["state"]["values"]["alternate_schedule_2"]["alternate_schedule_2-action"]["value"],
        "alternate_schedule_3": view["state"]["values"]["alternate_schedule_3"]["alternate_schedule_3-action"]["value"]
    }
    message_multiple_users(client, provided_emails, provided_schedules, windows_version)

app.view("windows_update_modal_view")(ack=respond_to_slack_within_3_seconds, lazy=[handle_shortcut_submission_events])

if __name__ == "__main__":      
    SocketModeHandler(app, SLACK_APP_TOKEN).start()