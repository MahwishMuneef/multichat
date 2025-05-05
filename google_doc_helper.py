from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

# If modifying these SCOPES, delete token.json
SCOPES = ['https://www.googleapis.com/auth/documents']

def get_google_docs_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("docs", "v1", credentials=creds)
    return service

def save_chat_to_google_doc(chat_messages):
    service = get_google_docs_service()
    doc_title = "Gemini Chat - Saved Conversation"

    # Create a new document
    doc = service.documents().create(body={"title": doc_title}).execute()
    doc_id = doc["documentId"]

    # Format chat into plain text
    content = ""
    for msg in chat_messages:
        role = msg["role"].capitalize()
        content += f"{role}: {msg['content']}\n\n"

    # Insert text
    requests = [
        {
            "insertText": {
                "location": {"index": 1},
                "text": content
            }
        }
    ]
    service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()

    doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
    return doc_url
