import json
import os

def lambda_handler(event, context):
    print("Authorizer event:", event)

    response = { 
        "isAuthorized": False,
    }

    headers = event.get("headers", {})
    api_key = headers.get("x-api-key")

    valid_api_keys = os.environ.get("API_KEYS", "").split(",")

    if api_key in valid_api_keys:
        response["isAuthorized"] = True

    return response
