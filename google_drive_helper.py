import os
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
FOLDER_NAME = "GeminiChatFiles"

def get_drive_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("drive", "v3", credentials=creds)
    return service

def get_or_create_folder(service, folder_name):
    results = service.files().list(
        q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'",
        fields="files(id, name)").execute()

    files = results.get("files", [])
    if files:
        return files[0]["id"]
    
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    folder = service.files().create(body=file_metadata, fields="id").execute()
    return folder["id"]

def save_chat_as_txt_to_drive(chat_messages):
    service = get_drive_service()
    folder_id = get_or_create_folder(service, FOLDER_NAME)

    # Create dynamic file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"chat_{timestamp}.txt"

    # Write to local file
    with open(filename, "w", encoding="utf-8") as f:
        for msg in chat_messages:
            role = msg["role"].capitalize()
            f.write(f"{role}: {msg['content']}\n\n")

    # Upload to Drive
    file_metadata = {
        "name": filename,
        "parents": [folder_id],
        "mimeType": "text/plain"
    }

    media = MediaFileUpload(filename, mimetype="text/plain")
    uploaded_file = service.files().create(
        body=file_metadata, media_body=media, fields="id, webViewLink").execute()

    # Clean up local file
    os.remove(filename)

    return uploaded_file.get("webViewLink")
