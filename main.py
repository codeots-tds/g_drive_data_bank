import pandas as pd
from g_data import *


def main(filename):
    data_files = load_json_data()
    selected_file_metadata = get_file_data(filename, data_files)
    file_data = download_file(filename, data_files)
    selected_file_name = selected_file_metadata['name']
    save_pickle_file(file_data, selected_file_metadata)
    desired_pickle_file_path = f'/home/ra-terminal/Desktop/portfolio_projects/g_drive_data_repo/pickle_files/{selected_file_name}.pickle'
    data = read_pickle_in_pandas(desired_pickle_file_path)
    print('success!')
    return data
    pass


if __name__ == '__main__':
    folder_id = 'root'
    filename = 'pokemon.csv'
    # get_all_files_metadata_to_json(folder_id)
    df = main(filename)
    print(df.head())
    # print(df.columns)
    pass