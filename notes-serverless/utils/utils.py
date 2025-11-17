import uuid
from datetime import datetime, timezone

# Return current time in ISO 8601 format with UTC timezone."""
def current_timestamp():
    
    return datetime.now(timezone.utc).isoformat()

# Generate a new note item with a unique ID and timestamp
def generate_note_item(username, title, text):
    
    note_id = str(uuid.uuid4())
    now = current_timestamp()

    return {
        'id': note_id,
        'username': username,
        'title': title,
        'text': text,
        'createdAt': now,
        'modifiedAt': now
    }

def build_update_expression(update_values):
    """
    Build a DynamoDB UpdateExpression, ExpressionAttributeValues, and ExpressionAttributeNames
    from a dict of fields to update.
    Handles reserved keywords like 'text' automatically.
    """
    update_expr_parts = []
    expr_attr_values = {}
    expr_attr_names = {}

    for key, value in update_values.items():
        placeholder_name = f"#{key}"
        placeholder_value = f":{key}"

        update_expr_parts.append(f"{placeholder_name} = {placeholder_value}")
        expr_attr_values[placeholder_value] = value
        expr_attr_names[placeholder_name] = key

    # Always update modifiedAt
    update_expr_parts.append("modifiedAt = :mod")
    expr_attr_values[":mod"] = current_timestamp()

    update_expr = "SET " + ", ".join(update_expr_parts)

    return update_expr, expr_attr_values, expr_attr_names
