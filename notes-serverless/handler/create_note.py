import json
from db.db import put_note
from utils.utils import generate_note_item

def lambda_handler(event, context):
    try:
        # Logging for CloudWatch
        print("EVENT RAW:", json.dumps(event)[:2000])

        # Path parameters pot fi None în HTTP API v2
        path_params = event.get('pathParameters') or {}
        username = path_params.get('username')

        # Body este string JSON în HTTP API v2; fallback corect este un string gol '{}'
        raw_body = event.get('body', '{}')
        # Dacă API Gateway ar trimite body deja ca dict, îl folosim direct
        if isinstance(raw_body, (dict, list)):
            body = raw_body
        else:
            body = json.loads(raw_body)

        # Ignorăm orice câmp furnizat de client care nu trebuie să vină din body
        title = body.get('title')
        text = body.get('text')

        # Validări clare
        if not username:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Username is required in path: /api/notes/{username}'})
            }
        if title is None or text is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing required fields: title and text'})
            }
        if not isinstance(title, str) or not isinstance(text, str):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Fields title and text must be strings'})
            }
        if len(title) > 50:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Title max 50 chars'})
            }
        if len(text) > 300:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Text max 300 chars'})
            }

        # Create a note — server creates id and timestamp
        note_item = generate_note_item(username, title, text)

        # Persistă în DynamoDB
        result = put_note(note_item)
        print("PUT RESULT:", json.dumps(result))

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Note created',
                'note': note_item
            })
        }

    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid JSON in request body'})
        }
    except Exception as e:
        # Logăm eroarea pentru CloudWatch
        print("UNEXPECTED ERROR:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error creating note', 'error': str(e)})
        }
