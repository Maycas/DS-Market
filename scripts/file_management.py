import os.path
import requests

# download Google Drive files helper functions
# useful as it doesn't use any Google third party libs, as we only want to download the data
# Adapted from https://stackoverflow.com/questions/25010369/wget-curl-large-file-from-google-drive/39225039#39225039


def get_file_id(gdrive_url):
    """
    Extracts the file ID from a Google Drive URL
    """
    return gdrive_url.split('/')[-2]


def get_confirm_token(response):
    """
    Gets the randomly generated confirm token by Google Drive
    """
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, destination):
    """
    Saves file contents from the response in the given destination
    """
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def download_file_from_google_drive(gdrive_url, destination):
    """
    Downloads and stores the file from the given url in the destination folder
    """
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    id = get_file_id(gdrive_url)
    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)
    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    save_response_content(response, destination)


# downloading and saving files

def download_files_from_url(urls, destination_directory, mode='gdrive'):
    """
    Downloads a list of files defined in the 'urls' dictionary inside 'destination_directory'.
    The 'urls' dictionary must have the keys 'filename' indicating how the file name that will 
    be used, and 'url', with the download URL link.
    """
    dir_list = []

    # transform dfs into a list if it's not
    if type(urls) != list:
        dfs = [urls]

    for url in urls:
        if not os.path.exists(destination_directory):
            print("Creating", destination_directory, "directory")
            os.makedirs(destination_directory)

        # downloading files
        file_name = url['filename']
        download_link = url['url']

        file_path = './' + destination_directory + '/' + file_name

        if not os.path.isfile(file_path):
            print("File doesn't exist. Downloading", file_name)
            if mode == 'gdrive':
                download_file_from_google_drive(download_link, file_path)
            else:
                pass
        else:
            print(file_name, "file already exists in", destination_directory)

        dir_list.append(file_path)
    return dir_list


def save_dfs_to_csv(dfs, destination_directory, prefix='', overwrite=True):
    """
    Gets an array of DataFrames 'dfs' and stores them in the given 'destination_directory'.
    The 'dfs' list is a list of dictionaries with 2 mandatory keys: 'filename' (as per the file name)
    and 'df' (containing the variable that will be converted to csv)
    Files can have a 'prefix' added if set.
    Returns a list of directories where the stored files can be found
    """
    dir_list = []

    # transform dfs into a list if it's not
    if type(dfs) != list:
        dfs = [dfs]

    for df in dfs:
        # check if destination_folder exists and creates it otherwise
        if not os.path.exists(destination_directory):
            print("Creating", destination_directory, "directory")
            os.makedirs(destination_directory)

        # creating the new files
        df_name = df['filename']
        df_data = df['df']

        file_path = './' + destination_directory + '/' + df_name
        if prefix:
            file_path += '_' + prefix
        file_path += '.csv'
        if not os.path.isfile(file_path):
            print(file_path, "doesn't exist. Creating new file")
        else:
            print(df_name, "file already exists in", destination_directory)
            if overwrite:
                print("Overwriting file")
                df_data.to_csv(file_path)

        dir_list.append(file_path)
    return dir_list
