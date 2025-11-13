# get_notes
import json
from db.db import get_notes_by_username

def lambda_handler(event, context):
    try:
        # Get username from path parameters
        username = event['pathParameters']['username']
        
        # Validation username
        if not username or not username.strip():
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Username is required'})
            }
        
        # Get notes from database
        notes = get_notes_by_username(username)
        
        # retuns a list with notes
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Notes retrieved successfully',
                'notes': notes
            })
        }
    
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Username parameter is missing'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error retrieving notes',
                'error': str(e)
            })
        }