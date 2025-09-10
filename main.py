import os
import json
import logging
import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
# custom py modules
import ui_templates
import aws_secrets
# Slack imports
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_sdk.errors import SlackApiError

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

SLACK_SIGNING_SECRET = aws_secrets.get_signing_secret()
SLACK_BOT_TOKEN = aws_secrets.get_bot_token()
SLACK_CANVAS = os.getenv("SLACK_CANVAS")
ALLOWED_USERS=os.getenv("ALLOWED_USERS").split(",")
LOG_CHANNEL=os.getenv("LOG_CHANNEL")


# Initializes your app with your bot token and signing secret
# https://api.slack.com/authentication/verifying-requests-from-slack
app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET,
    process_before_response=True
)
def get_todays_date() -> str:
    """Returns today's date in the format %Y-%m-%d %I:%M:%S %p %Z."""
    # Get the current datetime object
    now = datetime.datetime.now()
    # Convert to Pacific Time (Los Angeles)
    pacific_timezone = ZoneInfo("America/Los_Angeles") 
    now_aware = now.astimezone(pacific_timezone)
    formatted_datetime = now_aware.strftime("%Y-%m-%d %I:%M:%S %p %Z")
    return formatted_datetime

def respond_to_slack_within_3_seconds(ack):
    ack()

def handle_confirm_tentative(client, body, logger):
    try:
        logger.info(body)
        trigger_id=body["trigger_id"]
        private_metadata={
            "date":body["actions"][0]["value"],
            "message_ts":body["message"]["ts"],
            "user_id":body["container"]["channel_id"],
            "caller_id":body["message"]["user"]
        }
        confirmation_message=f':spiral_calendar_pad: I am scheduling my Windows upgrade on *{body["actions"][0]["value"]}*.'
        client.views_open(
            view=ui_templates.build_confirmation_modal(private_metadata, confirmation_message),
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
            "user_id": body["container"]["channel_id"],
            "caller_id":body["message"]["user"]
        }
        print(private_metadata)
        confirmation_message = f":spiral_calendar_pad: I am scheduling my Windows upgrade on *{selected_date}*"
        client.views_open(
            view=ui_templates.build_confirmation_modal(private_metadata, confirmation_message),
            trigger_id=trigger_id
        )
    except SlackApiError as e:
        logger.error(f"Failed to open modal: {e}")

reschedule_action_ids = [
    "confirm_reschedule_1",
    "confirm_reschedule_2",
    "confirm_reschedule_3",
    "confirm_reschedule_4",
    "confirm_reschedule_5"
]
for action_id in reschedule_action_ids:
    app.action(action_id)(ack=respond_to_slack_within_3_seconds, lazy=[handle_alternative_choice])

def handle_view_submission_events(body, client, logger):
    try:
        logger.info(body)
        private_metadata=json.loads(body["view"]["private_metadata"])
        #insert_at_end
        client.chat_update(
            channel=private_metadata["user_id"],
            ts=private_metadata["message_ts"],
            text=f"You have selected the week of {private_metadata['date']} for your {private_metadata['windows_version']} upgrade."
        )
        client.canvases_edit(
            canvas_id=SLACK_CANVAS,
            changes=[{"operation":"insert_at_end",
                    "document_content":{"type":"markdown","markdown":f"{private_metadata["windows_version"]}, {private_metadata['user_email']}, {private_metadata['date']}, {get_todays_date()}"}}]
        )
    except SlackApiError as e:
        logger.error(f"Failed to open modal: {e}")
app.view("confirmation_view")(ack=respond_to_slack_within_3_seconds, lazy=[handle_view_submission_events])

def handle_global_shortcut(body, client, logger):
    try:
        user_id = body["user"]["id"]
        if user_id not in ALLOWED_USERS:
            client.chat_postMessage(
                channel=user_id,
                text="You’re not authorized to use this shortcut. Contact #ask_bt if this seems wrong."
            )
            logger.info(f"Blocked {user_id}")
        else:
            client.views_open(
                trigger_id=body["trigger_id"],
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
            blocks=ui_templates.build_blocks_message(schedules, windows_version),
            text="Message from Endpoint Engineering"
        )
        ui_templates.update_confirmation_template({"user_email":email})
    except SlackApiError as e:
        client.chat_postMessage(
            channel=LOG_CHANNEL,
            markdown_text=f'''--------{windows_version}-------\nFailed for {email}: {e.response['error']}"'''
        )
        print(f"Failed for {email}: {e.response['error']}")

def message_multiple_users(client, emails: list[str], schedules:dict[str:str], windows_version:str):
    for email in emails: send_windows_message(client, email.strip(), schedules, windows_version) 


def handle_shortcut_submission_events(ack, body, client, logger, view):
    ack()
    logger.info(body)
    windows_version=view["state"]["values"]["windows_version"]["windows_version-action"]["value"]
    provided_emails=view["state"]["values"]["provided_emails"]["provided_emails-action"]["value"].split(",")
    provided_schedules={
        "windows_version":view["state"]["values"]["windows_version"]["windows_version-action"]["value"],
        "tentative_schedule": view["state"]["values"]["tentative_schedule"]["tentative_schedule-action"]["value"],
        "alternate_schedule_1": view["state"]["values"]["alternate_schedule_1"]["alternate_schedule_1-action"]["value"],
        "alternate_schedule_2": view["state"]["values"]["alternate_schedule_2"]["alternate_schedule_2-action"]["value"],
        "alternate_schedule_3": view["state"]["values"]["alternate_schedule_3"]["alternate_schedule_3-action"]["value"],
        "alternate_schedule_4": view["state"]["values"]["alternate_schedule_4"]["alternate_schedule_4-action"]["value"],
        "alternate_schedule_5": view["state"]["values"]["alternate_schedule_5"]["alternate_schedule_5-action"]["value"]
    }
    ui_templates.update_confirmation_template(provided_schedules)
    message_multiple_users(client, provided_emails, provided_schedules, windows_version)
app.view("windows_update_modal_view")(ack=respond_to_slack_within_3_seconds, lazy=[handle_shortcut_submission_events])

# AWS Lambda entrypoint
def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)