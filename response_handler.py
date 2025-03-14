from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests

class ResponseHandler:
    def __init__(self, slack_token="your-slack-bot-token", soar_url="http://soar-platform-url/api/trigger-playbook", api_token="your-api-token"):
        self.slack_client = WebClient(token=slack_token)
        self.soar_url = soar_url
        self.api_token = api_token

    def send_slack_alert(self, message, channel="#alerts"):
        try:
            response = self.slack_client.chat_postMessage(channel=channel, text=message)
            print("Slack alert sent:", response["ts"])
        except SlackApiError as e:
            print(f"Error sending Slack alert: {e}")

    def trigger_soar_playbook(self, anomaly_details):
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {"anomaly": anomaly_details}
        response = requests.post(self.soar_url, json=payload, headers=headers)
        if response.status_code == 200:
            print("SOAR playbook triggered successfully.")
        else:
            print("Failed to trigger SOAR playbook.")