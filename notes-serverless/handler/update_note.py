import json
from db.db import get_note_by_id, update_note

def lambda_handler(event, context):
    try:
        # Get note_id from path parameters
        note_id = event['pathParameters']['id']
        
        # Parse body request
        body = json.loads(event.get('body', '{}'))
        
        # Extract the field wich can be updated 
        title = body.get('title')
        text = body.get('text')
        
        # validation: at least one field is required 
        if title is None and text is None:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'At least one field (title or text) is required for update'})
            }
        
        # Validation lenght of the fields 
        if title and len(title) > 50:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Title max 50 chars'})
            }
            
        if text and len(text) > 300:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Text max 300 chars'})
            }
        
        # verify if the note exists before updating
        existing_note = get_note_by_id(note_id)
        if not existing_note:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Note not found'})
            }
        
        # get username from find note
        username = existing_note['username']
        
        # Get ready data for updating
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if text is not None:
            update_data['text'] = text
        
        # Update note in database 
        updated_note = update_note(username, note_id, update_data)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Note updated successfully',
                'note': updated_note['Attributes']
            })
        }
    
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Note ID parameter is missing'})
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid JSON in request body'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error updating note',
                'error': str(e)
            })
        }