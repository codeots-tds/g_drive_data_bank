import json 
import pandas as pd
from io import StringIO
import io
import sys
import pickle

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from googleapiclient.discovery import build
import google.auth
from googleapiclient.errors import HttpError
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from oauth2client.file import Storage

#clients secrets in local directory
# client_secrets_file_path = '/home/ra-terminal/Desktop/portfolio_projects/g_drive_data_repo/client_secret_1089494195663-b3paf99mi4gc07dgfchp3sq0ffhc18tk.apps.googleusercontent.com.json:Zone.Identifier'
# credentials_file_path = '/home/ra-terminal/Desktop/portfolio_projects/g_drive_data_repo/client_secrets.json'

client_secrets_file_path = '/home/ra-terminal/api_keys/google_key/g_drive_credentials/client_secret_1089494195663-b3paf99mi4gc07dgfchp3sq0ffhc18tk.apps.googleusercontent.com.json:Zone.Identifier'
credentials_file_path = '/home/ra-terminal/api_keys/google_key/g_drive_credentials/client_secrets.json'
client_secrets_file_path = credentials_file_path
gauth = GoogleAuth(client_secrets_file_path)
gauth.LoadClientConfigFile(client_secrets_file_path)
gauth = GoogleAuth()

# """
# Note that gauth.CommandLineAuth() is typically used in command-line applications 
# where a graphical user interface is not available. If you are building a graphical application, 
# you may want to use gauth.LocalWebserverAuth() instead, as it provides a more user-friendly authentication flow 
# that can be integrated into a web browser.
# """
## gauth.CommandLineAuth() #harder to configure but replaces localwebserverauth
gauth.LocalWebserverAuth() #creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

# file1 = drive.CreateFile({'title': 'Helloooooo.txt'}) #CREATE GOOGLEDRIVE
# file1.SetContentString('HELLOOOOOUHWUHDAOFAIEFEHBEBFSWF')
# file1.Upload()


"""generates a really complicated json datastructure"""
def get_all_files_metadata_to_json(folder_id):
    file_list = []
    page_token = None
    files = drive.ListFile({'q': "'%s' in parents and trashed=false" % folder_id}).GetList()    
    check_keys = ['fileSize', 'downloadUrl']
    for idx, file in enumerate(files):
        print(idx)
        file_id = file['id']
        file_name = file['title']
        file_type = file['mimeType']
        file_owners = file['owners']
        parent = file['parents']
        if file_type == 'application/vnd.google-apps.folder':
            sub_files = get_all_files_metadata_to_json(file_id)
            file_list.append({'name': file_name,
                                'type': 'folder',
                                'folder_id': folder_id,
                                # 'owners': file_owners,
                                # 'parent': parent,
                                'contents': sub_files,
                                })
        else:
            file_list.append({'name': file_name,
                              'type': 'file_type',
                              'id': file_id,
                            #   'owners': file_owners,
                            #   'parent': parent,
                              })
    
    # dumping results into json
    json_data_path = '/home/ra-terminal/Desktop/portfolio_projects/g_drive_data_repo/g_drive_metadata.json'
    with open(json_data_path, 'w') as f_obj:
        json.dump(file_list, f_obj, indent=2)
    return file_list

def load_json_data():
    with open('/home/ra-terminal/Desktop/portfolio_projects/g_drive_data_repo/g_drive_metadata.json', 'r') as f_obj:
        data_files = json.load(f_obj)
    return data_files

def get_file_data(file_target, data_files):
    for idx, file in enumerate(data_files):
        file_name = file['name']
        file_type = file['type']
        if file_type == 'folder':
            content = get_file_data(file_target = file_target, data_files = file['contents'])
            if content:
                return content
        elif file_type == 'file_type':
            if file['name'] == file_target:
                return file #doesn't return file though
            

def download_file(filename, json_data):
    file_metadata = get_file_data(filename, data_files=json_data)
    file_id = file_metadata['id']
    file_name = file_metadata['name']
    # mimeType = file_metadata['mimeType']
    target_file = drive.CreateFile({'id':file_id})
    print("Target file is: -------------->>>", target_file)
    target_download = target_file.GetContentString(file_metadata['name'])
    return target_download

def save_pickle_file(str_content, file):
    filename = file['name']
    pickle_path = f'/home/ra-terminal/Desktop/portfolio_projects/g_drive_data_repo/pickle_files/{filename}.pickle'
    try:
        with open(pickle_path, 'wb') as f:
            # load the pickle object
            pickle.dump(str_content, f)
    except error.PickleError as error:
         print(f'An error has occurred: {error}')
         

def read_pickle_in_pandas(filepath):
    data_obj = pickle.load(open(filepath, 'rb'))
    df = pd.read_csv(io.StringIO(data_obj))
    return df

if __name__ == "__main__":
    root_file_id = 'root'

    data_files = load_json_data()
    selected_file = get_file_data(file_target="pokemon.csv", data_files = data_files)
    file_data = download_file('pokemon.csv', data_files)
    save_pickle_file(file_data, selected_file)

    selected_file_name = selected_file['name']
    desired_pickle_file_path = f'/home/ra-terminal/Desktop/portfolio_projects/g_drive_data_repo/pickle_files/{selected_file_name}.pickle'
    data = read_pickle_in_pandas(desired_pickle_file_path)
    # print(data.columns)
    print('complete run')
    pass