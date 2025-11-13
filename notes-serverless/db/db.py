import boto3
from boto3.dynamodb.conditions import Key

# DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Reference to notes table
notes_table = dynamodb.Table('notes')

# Insert a new note into the DynamoDB table
def put_note(note_item):
    return notes_table.put_item(Item = note_item)

# Query notes by username.
def get_notes_by_username(username):

    response = notes_table.query(
        KeyConditionExpression=Key('username').eq(username)  
    )
    return response.get('Items', [])

# Scan to find note by unique ID.
def get_note_by_id(note_id):
    
    response = notes_table.scan(
        FilterExpression='id = :id',
        ExpressionAttributeValues={':id': note_id}
    )
    items = response.get('Items', [])
    return items[0] if items else None

# Update note fields and modifiedAt timestamp.
# update_values: dict with keys like title, text
def update_note(note_id, update_values):
    
    update_expr = "SET "
    expr_attr_values = {}

    # Add only fields than can be modified 
    if 'title' in update_values:
        update_expr += "title = :title, "
        expr_attr_values[':title'] = update_values['title']
    
    if 'text' in update_values:
        update_expr += "text = :text, "
        expr_attr_values[':text'] = update_values['text']
    
    #  modifiedAt
    from datetime import datetime, timezone
    update_expr += "modifiedAt = :mod"
    expr_attr_values[':mod'] = datetime.now(timezone.utc).isoformat()

    return notes_table.update_item(
        Key={'id': note_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_attr_values,
        ReturnValues="ALL_NEW"
    )

# Delete a note by its unique ID.
def delete_note(note_id):
    
    return notes_table.delete_item(Key={'id': note_id})