import requests

class SlackAPI:
    
    def postMessage11(chennel):

        headers = {
            'Authorization': '',
            # Already added when you pass json= but not when you pass data=
            # 'Content-type': 'application/json',
        }

        json_data = {
            'channel': chennel,
            	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Test block with multi conversations select"
			},
			"accessory": {
				"type": "multi_conversations_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select conversations",
				},
				"action_id": "multi_conversations_select-action"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "This is a section block with a button."
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Click Me",
				},
				"value": "click_me_123",
				"action_id": "button-action"
			}
		},
		{
			"type": "input",
			"element": {
				"type": "radio_buttons",
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",

						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",

						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",

						},
						"value": "value-2"
					}
				],
				"action_id": "radio_buttons-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Label",

			}
		}
	]


        }

        response = requests.post('https://slack.com/api/chat.postMessage', headers=headers, json=json_data)

        return response

    def postMessage(chennel,text):

        headers = {
            'Authorization': '',
            # Already added when you pass json= but not when you pass data=
            # 'Content-type': 'application/json',
        }

        json_data = {
            'channel': chennel,
            'text': text,    
            }

        response = requests.post('https://slack.com/api/chat.postMessage', headers=headers, json=json_data)

        return response



