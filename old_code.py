# storage = file.Storage(client_secrets_file_path)
# credentials = storage.get()
# http = credentials.authorize(Http())
# drive=discovery.build('drive', 'v3', http=http)
# drive api service
# defining path variables:
# client_secrets_file_path = '/home/ra-terminal/api_keys/google_key/credentials/client_secret_key.googleusercontent.com.json'
# storage = file.Storage(client_secrets_file_path)
# print("store", storage)
# print(type(storage))

# get access token
# credentials = storage.get()
# # print(credentials, '====')
# http = credentials.authorize(Http())
# drive=discovery.build('drive', 'v3', http=http)


def get_all_files_to_json(drive):
    results = []
    page_token = None

    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = drive.files().list(**param).execute()            # append the files from the current result page to our list
            results.extend(files.get('files'))            # Google Drive API shows our files in multiple pages when the number of files exceed 100
            page_token = files.get('nextPageToken')

            if not page_token:
                break
        except error.HttpError as error:
            print(f'An error has occurred: {error}')
            break    # output the file metadata to console
    
    #dumping results into json
    with open('/home/ra-terminal/Desktop/portfolio_projects/g_drive_data_repo/g_drive_metadata.json', 'w') as f_obj:
        json.dump(results, f_obj, indent=2)
    return results

# def get_file_download(filename):
#     file_metadata = search_file(filename)
#     # file_id = file_metadata['id']
#     # file_name = file_metadata['name']
#     # mimeType = file_metadata['mimeType']
#     target_file = drive.CreateFile({'id':file_metadata['id']})
#     print("Target file is: -------------->>>", target_file)
#     target_download = target_file.GetContentString(file_metadata['name'])
#     return target_download


"""2nd to last attempt to approach recursive iteration"""
def get_file(file_target, data_files):
    single_files = []
    single_file_entries = []
    if isinstance(data_files, dict):
        for key, file_content in data_files.items():
            if key != 'contents':
                name_temp = file_content
                single_file_entries.append(file_content)
                if len(single_file_entries) == 3:
                    single_files.append(single_file_entries)
            elif key == 'contents':
                # get_file(file_target, data_files = file_content)
                return get_file(file_target, data_files = file_content)
    elif isinstance(data_files, list):
        for idx, file in enumerate(data_files):
            file_name = file['name']
            if file_name != file_target:
                # get_file(file_target = file_target, data_files = file)
                return get_file(file_target = file_target, data_files = file)
            elif file_name == file_target:
                print(file, 'prints')
                return file #doesn't return file though
    # print(single_files) 
    # return single_files














def get_file(file_target, data_files):
    single_files = []
    single_file_entries = []
    if isinstance(data_files, dict):
        for key, file_content in data_files.items():
            if key != 'contents':
                name_temp = file_content
                single_file_entries.append(file_content)
                if len(single_file_entries) == 3:
                    single_files.append(single_file_entries)
            elif key == 'contents':
                # get_file(file_target, data_files = file_content)
                return get_file(file_target, data_files = file_content)
    elif isinstance(data_files, list):
        for idx, file in enumerate(data_files):
            file_name = file['name']
            if file_name != file_target:
                # get_file(file_target = file_target, data_files = file)
                return get_file(file_target = file_target, data_files = file)
            elif file_name == file_target:
                print(file, 'prints')
                return file #doesn't return file though
    # print(single_files) 
    # return single_files

    """adding some test lines here"""