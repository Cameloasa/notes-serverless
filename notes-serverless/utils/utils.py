import uuid
from datetime import datetime, timezone

def generate_note_item(username, title,text):
    # Generate a new note item with a unique ID and timestamp

    note_id = str(uuid.uuid4())
    # now =  datetime.now(timezone.utc).isoformat()
    now = str(datetime.now())

    return {
        'id': note_id,
        'username': username,
        'title': title,
        'text': text,
        'createdAt': now,
        'modifiedAt': now
    }
