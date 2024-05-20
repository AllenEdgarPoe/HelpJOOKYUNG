import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import configparser

properties = configparser.ConfigParser()
properties.read('authentication.ini')
slack_api_key = properties['SLACK_AUTH']['slack_key']
client = WebClient(token=slack_api_key)

def check_channel_id(channel_name):
    channel_name = channel_name
    conversation_id = None
    try:
        # Call the conversations.list method using the WebClient
        for result in client.conversations_list():
            if conversation_id is not None:
                break
            for channel in result["channels"]:
                if channel["name"] == channel_name:
                    conversation_id = channel["id"]
                    #Print result
                    print(f"Found conversation ID: {conversation_id}")
                    break
        print(conversation_id)
        return conversation_id

    except SlackApiError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_channel_id('sdv-or-animatediff')
