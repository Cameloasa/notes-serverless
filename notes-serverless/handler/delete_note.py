import json
from db.db import get_note_by_id, delete_note

def lambda_handler(event, context):
    try:
        # get note_id din path parameters
        note_id = event['pathParameters']['id']
        
        # Validation note_id
        if not note_id or not note_id.strip():
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Note ID is required'})
            }
        
        # Verify if note exists before delete 
        existing_note = get_note_by_id(note_id)
        if not existing_note:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Note not found'})
            }
        
        # Delete note from database
        delete_note(note_id)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Note deleted successfully',
                'deletedNote': existing_note
            })
        }
    
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Note ID parameter is missing'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error deleting note',
                'error': str(e)
            })
        }