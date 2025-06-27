import json
import requests

# This is a public key and exposed in web anyway, no worry about it in code.
AMPLITUDE_API_KEY = "e8fbd42ed1d90d161e89c5b0a8114d87"

def send_bedrock_amplitude_event(user_id, callType, model, bedrock_response, event_properties=None):
    headers = bedrock_response['ResponseMetadata']['HTTPHeaders']

    if event_properties is None:
        event_properties = {}

    event_properties["callType"] = callType
    event_properties["model"] = model
    event_properties["inputTokens"] = int(headers.get('x-amzn-bedrock-input-token-count', 0))
    event_properties["outputTokens"] = int(headers.get('x-amzn-bedrock-output-token-count', 0))
    event_properties["latency"] = int(headers.get('x-amzn-bedrock-invocation-latency', 0))

    send_amplitude_event(user_id, "bedrock_call", event_properties)

def send_amplitude_event(user_id, event_type, event_properties=None):
    if event_properties is None:
        event_properties = {}

    event_properties["environment"] = "dev.firewhisper.io"


    payload = {
        "api_key": AMPLITUDE_API_KEY,
        "events": [
            {
                "user_id": user_id,
                "event_type": event_type,
                "event_properties": event_properties,
            }
        ],
    }

    response = requests.post(
        "https://api2.amplitude.com/2/httpapi",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )

    if response.status_code != 200:
        print("Amplitude error:", response.text)
    else:
        print("Event sent to Amplitude:", response.json())