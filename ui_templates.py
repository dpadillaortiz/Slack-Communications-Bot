from typing import Dict, Any
from copy import deepcopy
import json

MODAL_CONFIRMATION_TEMPLATE: Dict[str, Any] = {
	"type": "modal",
	"submit": {
		"type": "plain_text",
		"text": "Confirm",
		"emoji": True
	},
	"private_metadata": False,
	"close": {
		"type": "plain_text",
		"text": "Go Back",
		"emoji": True
	},
	"title": {
		"type": "plain_text",
		"text": "Confirm Your Schedule",
		"emoji": True
	},
	"callback_id": "confirmation_view",
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": ":point_right: Please review your selection below."
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"block_id": "confirmation_message",
			"text": {
				"type": "mrkdwn",
				"text": "confirmation_message"
			}
		}
	]
}


SHORTCUT_MODAL_TEMPLATE: Dict[str, Any] = {
	"title": {
		"type": "plain_text",
		"text": "My App",
		"emoji": True
	},
	"callback_id": "windows_update_modal_view",
	"submit": {
		"type": "plain_text",
		"text": "Submit",
		"emoji": True
	},
	"type": "modal",
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"private_metadata": False,
	"blocks": [
		{
			"type": "input",
			"block_id": "windows_version",
			"element": {
				"type": "plain_text_input",
				"action_id": "windows_version-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Windows Version",
				"emoji": True
			}
		},
		{
			"type": "input",
			"block_id": "provided_emails",
			"element": {
				"type": "plain_text_input",
				"multiline": True,
				"action_id": "provided_emails-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Please provide a list of emails separated by a comma",
				"emoji": True
			}
		},
		{
			"type": "input",
			"block_id": "tentative_schedule",
			"element": {
				"type": "plain_text_input",
				"action_id": "tentative_schedule-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Tentative Schedule",
				"emoji": True
			}
		},
		{
			"type": "input",
			"block_id": "alternate_schedule_1",
			"element": {
				"type": "plain_text_input",
				"action_id": "alternate_schedule_1-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Alternate Schedule 1",
				"emoji": True
			}
		},
		{
			"type": "input",
			"block_id": "alternate_schedule_2",
			"element": {
				"type": "plain_text_input",
				"action_id": "alternate_schedule_2-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Alternate Schedule 2",
				"emoji": True
			}
		},
		{
			"type": "input",
			"block_id": "alternate_schedule_3",
			"element": {
				"type": "plain_text_input",
				"action_id": "alternate_schedule_3-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Alternate Schedule 3",
				"emoji": True
			}
		}
	]
}

BLOCK_MESSAGE_TEMPLATE: Dict[str, Any] = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Time to Schedule Your Windows 11 24H2 Upgrade"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "screen_1_message"
			}
		},
		{
			"type": "actions",
			"block_id": "scheduled_date",
			"elements": [
				{
					"type": "button",
					"action_id": "confirm_date",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "This week works for me"
					},
					"style": "primary",
					"value": "confirm_date-value"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Need a different time?*"
			}
		},
		{
			"type": "section",
			"block_id": "alternate_1",
			"text": {
				"type": "mrkdwn",
				"text": "alternate_1"
			},
			"accessory": {
				"type": "button",
				"action_id": "confirm_reschedule_1",
				"text": {
					"type": "plain_text",
					"emoji": True,
					"text": "Choose"
				},
				"value": "alternate_1-date"
			}
		},
		{
			"type": "section",
			"block_id": "alternate_2",
			"text": {
				"type": "mrkdwn",
				"text": "alternate_2"
			},
			"accessory": {
				"type": "button",
				"action_id": "confirm_reschedule_2",
				"text": {
					"type": "plain_text",
					"emoji": True,
					"text": "Choose"
				},
				"value": "alternate_2-date"
			}
		},
		{
			"type": "section",
			"block_id": "alternate_3",
			"text": {
				"type": "mrkdwn",
				"text": "alternate_3"
			},
			"accessory": {
				"type": "button",
				"action_id": "confirm_reschedule_3",
				"text": {
					"type": "plain_text",
					"emoji": True,
					"text": "Choose"
				},
				"value": "alternate_3-date"
			}
		}
	]
}

def update_confirmation_template(private_metadata:dict):
	if MODAL_CONFIRMATION_TEMPLATE["private_metadata"] == False:
		MODAL_CONFIRMATION_TEMPLATE["private_metadata"] = private_metadata
	else:
		MODAL_CONFIRMATION_TEMPLATE["private_metadata"].update(private_metadata)

def build_confirmation_modal(private_metadata: dict, confirmation_message: str):
    print(MODAL_CONFIRMATION_TEMPLATE)
    confirmation_modal = deepcopy(MODAL_CONFIRMATION_TEMPLATE)
    confirmation_modal["blocks"][2]["text"]["text"] = confirmation_message
    x_private_metadata = confirmation_modal["private_metadata"]
    print("---------------LOOK AT ME-----------------")
    print("x_private_metadata type", type(x_private_metadata))
    print("x_private_metadata:", x_private_metadata)
    x_private_metadata.update(private_metadata)
    print("---------------LOOK AT ME-----------------")
    print("x_private_metadata type", type(x_private_metadata))
    print("x_private_metadata:", x_private_metadata)
    confirmation_modal["private_metadata"] = json.dumps(x_private_metadata)
    return confirmation_modal


def build_shortcut_modal(private_metadata: str):
    shortcut_modal = deepcopy(SHORTCUT_MODAL_TEMPLATE)
    shortcut_modal["private_metadata"]=json.dumps(private_metadata)
    return shortcut_modal

def build_blocks_message(provided_schedules:dict, windows_version:str):
	screen_1_message = f"Hi Workmate :wave:\nTo keep your Workday-managed laptop secure and up-to-date, we're getting it ready for an upgrade to *{windows_version}*. We have tentatively scheduled yours for the week of *{provided_schedules['tentative_schedule']}*.\n\n You can approve this time or choose a different week below. If you don't make a selection, your upgrade will proceed during this assigned week.\n\n*What to Expect:*\n- The upgrade will download in the background with no interruption to your work.\n- You'll receive a prompt to restart your device once the download is complete.\n- The final installation takes about 45 minutes after you restart, and your device will be unavailable during this time.\n- *Heads-up:* If you don't restart within 7 days of the prompt, your device will restart automatically to complete the upgrade."
	blocks_message = deepcopy(BLOCK_MESSAGE_TEMPLATE)["blocks"]
	blocks_message[0]["text"]["text"]=f"Time to Schedule Your {windows_version} Upgrade"
	blocks_message[1]["text"]["text"]=screen_1_message
	blocks_message[2]["elements"][0]["value"]=provided_schedules["tentative_schedule"]

	blocks_message[5]["text"]["text"]=f"Upgrade the week of *{provided_schedules['alternate_schedule_1']}*"
	blocks_message[5]["accessory"]["value"]=provided_schedules["alternate_schedule_1"]

	blocks_message[6]["text"]["text"]=f"Upgrade the week of *{provided_schedules['alternate_schedule_2']}*"
	blocks_message[6]["accessory"]["value"]=provided_schedules["alternate_schedule_2"]

	blocks_message[7]["text"]["text"]=f"Upgrade the week of *{provided_schedules['alternate_schedule_3']}*"
	blocks_message[7]["accessory"]["value"]=provided_schedules["alternate_schedule_3"]

	print("---------------LOOK AT ME-----------------")
	print("blocks_message type", type(blocks_message))
	return blocks_message