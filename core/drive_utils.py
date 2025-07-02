from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials


def authenticate_drive(service_account_json_path):
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
