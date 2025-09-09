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
		},
		{
			"type": "input",
			"block_id": "alternate_schedule_4",
			"element": {
				"type": "plain_text_input",
				"action_id": "alternate_schedule_4-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Alternate Schedule 4",
				"emoji": True
			}
		},
		{
			"type": "input",
			"block_id": "alternate_schedule_5",
			"element": {
				"type": "plain_text_input",
				"action_id": "alternate_schedule_5-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Alternate Schedule 5",
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
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":point_down: *Select a different week:*"
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
		},
		{
			"type": "section",
			"block_id": "alternate_4",
			"text": {
				"type": "mrkdwn",
				"text": "alternate_4"
			},
			"accessory": {
				"type": "button",
				"action_id": "confirm_reschedule_4",
				"text": {
					"type": "plain_text",
					"emoji": True,
					"text": "Choose"
				},
				"value": "alternate_4-date"
			}
		},
		{
			"type": "section",
			"block_id": "alternate_5",
			"text": {
				"type": "mrkdwn",
				"text": "alternate_5"
			},
			"accessory": {
				"type": "button",
				"action_id": "confirm_reschedule_5",
				"text": {
					"type": "plain_text",
					"emoji": True,
					"text": "Choose"
				},
				"value": "alternate_5-date"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "screen_message_part_2"
			}
		},
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

	screen_message_part_1 = f"""
	Hello Workmate,\n
	We are upgrading your Workday laptop to {windows_version} for improved performance and enhanced security.\n\n
	Your upgrade is scheduled for the week of Month XX–XX, 2025. If this timing works for you, no action is required.\n\n
	If you need to select a different week, please choose from the options below by Friday, Month 12 at 6:00 PM PT.\n\n
	"""
	screen_message_part_2 = f"""		   
	:gear: The Upgrade Process\n
	The process is designed to accommodate your schedule. Here's how it works:\n
	* *Background Download:* On Monday, September XX, the update will download in the background without interrupting your work.
	* *Restart Prompt:* Once the download is complete, you'll be prompted to restart. You can choose to:
		* *Restart now*
		* *Schedule a specific time*
		* *Restart tonight* (7:00 PM your local time)
	* *Recommended Timing:* We suggest restarting at the end of your workday or overnight to avoid conflicts with meetings or deadlines.
	* *45-Minute Installation:* The upgrade takes approximately 45 minutes after you restart. Your laptop must remain plugged in during this time.
	* *Automatic Restart:* Your laptop will automatically restart to complete the upgrade if you do not restart within your 7-day window.
	
	:sparkles: Benefits of {windows_version}\n
	This update introduces several key improvements to enhance your work experience:\n
	* *Faster Performance:* Noticeably quicker boot times and application launches.
	* *Improved Workflow:* Organize your work with a tabbed File Explorer and find what you need faster with a more powerful search.
	* *Enhanced Security:* Adds a new layer of data encryption to provide extra protection for your work.
	* *Extended Battery Life:* New efficiency modes help you work longer when unplugged.
	* *Stronger Connectivity:* Benefit from the latest Wi-Fi standards for a faster, more stable connection.
	
	:handshake: Support\n
	During your upgrade week, you will be added to a dedicated Slack channel for direct support from the BT team.\n\n
	For additional questions, please refer to the [{windows_version} FAQ] or ask in #ask-bt.\n\n
	Thank you,\n
	BT Infrastructure
	"""
	# screen_1_message = f"Hi Workmate :wave:\nTo keep your Workday-managed laptop secure and up-to-date, we're getting it ready for an upgrade to *{windows_version}*. We have tentatively scheduled yours for the week of *{provided_schedules['tentative_schedule']}*.\n\n You can approve this time or choose a different week below. If you don't make a selection, your upgrade will proceed during this assigned week.\n\n*What to Expect:*\n- The upgrade will download in the background with no interruption to your work.\n- You'll receive a prompt to restart your device once the download is complete.\n- The final installation takes about 45 minutes after you restart, and your device will be unavailable during this time.\n- *Heads-up:* If you don't restart within 7 days of the prompt, your device will restart automatically to complete the upgrade."
	blocks_message = deepcopy(BLOCK_MESSAGE_TEMPLATE)["blocks"]
	blocks_message[0]["text"]["text"]=f":windows_logo: Your Windows 11 Upgrade: Scheduled for {provided_schedules["tentative_schedule"]} :windows_logo:"
	blocks_message[1]["text"]["text"]=screen_message_part_1
	# blocks_message[2]["elements"][0]["value"]=provided_schedules["tentative_schedule"]

	blocks_message[3]["text"]["text"]=f"Upgrade the week of *{provided_schedules['alternate_schedule_1']}*"
	blocks_message[3]["accessory"]["value"]=provided_schedules["alternate_schedule_1"]

	blocks_message[4]["text"]["text"]=f"Upgrade the week of *{provided_schedules['alternate_schedule_2']}*"
	blocks_message[4]["accessory"]["value"]=provided_schedules["alternate_schedule_2"]

	blocks_message[5]["text"]["text"]=f"Upgrade the week of *{provided_schedules['alternate_schedule_3']}*"
	blocks_message[5]["accessory"]["value"]=provided_schedules["alternate_schedule_3"]

	blocks_message[6]["text"]["text"]=f"Upgrade the week of *{provided_schedules['alternate_schedule_4']}*"
	blocks_message[6]["accessory"]["value"]=provided_schedules["alternate_schedule_4"]

	blocks_message[7]["text"]["text"]=f"Upgrade the week of *{provided_schedules['alternate_schedule_5']}*"
	blocks_message[7]["accessory"]["value"]=provided_schedules["alternate_schedule_5"]

	blocks_message[8]["text"]["text"]=screen_message_part_2

	print("---------------LOOK AT ME-----------------")
	print("blocks_message type", type(blocks_message))
	return blocks_message