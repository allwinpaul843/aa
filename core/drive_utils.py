from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import json

def authenticate_drive(service_account_json_path):
    # Debug: Check the contents of the service account file before loading
    with open(service_account_json_path, 'r') as f:
        try:
            credentials = json.load(f)
            print("Service account JSON loaded successfully.")
        except json.JSONDecodeError as e:
            print(f"Error loading JSON: {e}")
            f.seek(0)
            print(f"Invalid JSON content:\n{f.read()}")
            raise e

    gauth = GoogleAuth()
    gauth.auth_method = 'service'
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        service_account_json_path,
        ['https://www.googleapis.com/auth/drive']
    )
    return GoogleDrive(gauth)

def download_file_from_drive(drive, file_id, dest_path):
    file = drive.CreateFile({'id': file_id})
    file.GetContentFile(dest_path)

def upload_file_to_drive(drive, file_id, src_path):
    file = drive.CreateFile({'id': file_id})
    file.SetContentFile(src_path)
    file.Upload()
