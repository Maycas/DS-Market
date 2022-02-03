import os.path


def save_dfs_to_csv(dfs, destination_directory, prefix=''):
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
            print("Overwriting file")
        df_data.to_csv(file_path)

        dir_list.append(file_path)
    return dir_list
