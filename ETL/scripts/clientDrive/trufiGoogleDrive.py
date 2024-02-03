from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import FileNotUploadedError
import os

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)
credentials_directory = os.path.join(script_directory, 'credentials_module.json')

def login():
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = credentials_directory
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credentials_directory)
    
    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
        
    gauth.SaveCredentialsFile(credentials_directory)
    credentials = GoogleDrive(gauth)
    return credentials

def create_text_file(file_name, content, folder_id):
    credentials = login()
    file = credentials.CreateFile({'title': file_name,\
                                   'parents': [{"kind": "drive#fileLink",\
                                                "id": folder_id}]})
    file.SetContentString(content)
    file.Upload()

def download_file_by_name(file_name, download_path):
    credentials = login()
    files = credentials.ListFile({'q': "title = '" + file_name + "'"}).GetList()
    if not files:
        print('File not found: ' + file_name)
    file = credentials.CreateFile({'id': files[0]['id']}) 
    file.GetContentFile(download_path + file_name)

def compare_download_files(name_list, folder_id, local_download_path):
    credentials = login()
    drive_files = credentials.ListFile({'q': f"'{folder_id}' in parents"}).GetList()
    drive_names = [file['title'] for file in drive_files]
    files_to_download = [name for name in drive_names if name not in name_list]

    if not files_to_download:
        print("No files to download.")
        return

    for file_name in files_to_download:
        if any(file['title'] == file_name for file in drive_files):
            download_file_by_name(file_name, local_download_path)
            print(f"File '{file_name}' downloaded to '{local_download_path}'")
        else:
            print(f"Warning: File '{file_name}' no longer exists in Google Drive.")

def get_file_list_from_directory(directory):
    file_list = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    return file_list

if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    logs_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(script_path)))), 'Datos', 'Logs//')
    file_list = get_file_list_from_directory(logs_directory)
    folder_id = '1kr1V8vkL_iIzfZ5WMZQgpmiF_AsPBWRd'
    local_download_path = logs_directory
    compare_download_files(file_list, folder_id, local_download_path)