import boto3
from boto3.dynamodb.conditions import Key
from utils.utils import current_timestamp
from utils.utils import build_update_expression

# DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Reference to notes table
notes_table = dynamodb.Table('notes-serverless-dev')

# Insert a new note into the DynamoDB table
def put_note(note_item):
    return notes_table.put_item(Item = note_item)

# Query notes by username.
def get_notes_by_username(username):

    response = notes_table.query(
        KeyConditionExpression=Key('username').eq(username)  
    )
    return response.get('Items', [])


def get_note_by_id(note_id):
    response = notes_table.query(
        IndexName='idIndex',
        KeyConditionExpression=Key('id').eq(note_id)
    )
    items = response.get('Items', [])
    return items[0] if items else None

# Update note fields and modifiedAt timestamp.
# update_values: dict with keys like title, text
def update_note(username, note_id, update_values):
    update_expr, expr_attr_values, expr_attr_names = build_update_expression(update_values)

    return notes_table.update_item(
        Key={'username': username, 'id': note_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_attr_values,
        ExpressionAttributeNames=expr_attr_names,
        ReturnValues="ALL_NEW"
    )

# Delete a note by its unique ID.
def delete_note(username, note_id):
    return notes_table.update_item(
        Key={'username': username, 'id': note_id},
        UpdateExpression="SET deletedAt = :del",
        ExpressionAttributeValues={':del': current_timestamp()},
        ReturnValues="ALL_NEW"
    )
