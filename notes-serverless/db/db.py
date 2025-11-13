import boto3

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
        KeyConditionExpression='username = :u',
        ExpressionAttributeValues={':u': username}
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
    for i, (key, value) in enumerate(update_values.items()):
        placeholder = f":val{i}"
        update_expr += f"{key} = {placeholder}, "
        expr_attr_values[placeholder] = value

    update_expr += "modifiedAt = :mod"
    expr_attr_values[":mod"] = update_values.get("modifiedAt")

    return notes_table.update_item(
        Key={'id': note_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_attr_values,
        ReturnValues="ALL_NEW"
    )

# Delete a note by its unique ID.
def delete_note(note_id):
    
    return notes_table.delete_item(Key={'id': note_id})