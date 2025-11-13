import json
from db.db import put_note
from utils.utils import generate_note_item

def lambda_handler(event, context):

    try:
        username = event['pathParameters'].get('username')
        body = json.loads(event.get('body', {}))

        title = body.get('title')
        text = body.get('text')

        # Validation
        if not username or not title or not text:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Title max 50 chars, text max 300 chars'})
            }
        
        if len(title) > 50:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Title max 50 chars'})
            }
            
        if len(text) > 300:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'Text max 300 chars'
                    })
            }
        
        # create note
        note_item = generate_note_item(username, title, text)

        # Save in dynamodb
        put_note(note_item)

        return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Note created', 
                    'note': note_item
                    })
            }
    
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Invalid JSON in request body'
                })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error creating note', 
                'error': str(e)
                })
        }

        

