import os
import json


def authorizer(event, context):
    """
    Custom authorizer for validation of API Key
    """

    print("Authorizer called")

    # Extract API Key from header
    api_key = event.get('headers', {}).get('x-api-key')
    print(f"Received API Key: {api_key}")
    
    # Take API Key valide from environment variables
    valid_api_keys_str = os.environ.get('API_KEYS', '')
    print(f"Valid keys from env: {valid_api_keys_str}")  # Debug
    
    #  string into list
    valid_api_keys = [key.strip() for key in valid_api_keys_str.split(',')]
    
    if api_key and api_key in valid_api_keys:
        # API Key valid - allow access
        print("API Key valid - access granted") 
        return {
            'isAuthorized': True,
            'context': {
                'apiKey': api_key
            }
        }
    else:
        # API Key invalid - deny access
        print("API Key invalid - access denied")
        return {
            'isAuthorized': False
        }