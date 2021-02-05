def displayText():
    print( "Geeks 4 Geeks!")

class SlackMessage:
    def __init__(self):
        self.blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":calendar: |   *UPCOMING EVENTS*  | :calendar: "
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":mask: These dates and locations are available for registration of the COVID vaccine.",
                }
            },
            {
			    "type": "divider"
            }
        ]
    def appendSection(self, company, date, location, provider, link ):
        self.blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*({0})* - `{1}` \n{2} \n_{3}_".format(company, date, location, provider)
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Register",
                    },
                    "value": "click_me_123",
                    "url": link,
                    "action_id": "button-action"
                },
		    },     
        )
        self.blocks.append( 
            {
			    "type": "divider"
            }
        )
