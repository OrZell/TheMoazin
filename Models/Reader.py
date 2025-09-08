import datetime
import pathlib
import os


class Reader:

    def __init__(self):
        self.MainDirPath = os.getenv('MAIN_DATA_PATH')   # MainDirPath holds the var of the env MAIN_DATA_PATH
                                                         # that means the path of the main podcats dir (didn't give default)


    # the main method that returns finally list with the details each file
    def get_list_of_details(self):
        lst_of_details = self.loop_through_path_and_create_dct_of_details()
        return lst_of_details

    # method that loop through all files in dir (i thought filter it by *wav but didn't) and create dict
    # key is the name of the file and the value is dict with keys 'metadata' and 'file_path'
    def loop_through_path_and_create_dct_of_details(self):
        if self.MainDirPath is None:
            raise Exception('Path Not Exist')

        path = pathlib.Path(self.MainDirPath)
        dct_with_details = {}

        for subdir in path.iterdir():
            stats = os.stat(subdir)

            dct_with_details[subdir.name] = {}

            details = {
                'file_name': subdir.name,
                'size_kb': self.formating_file_size_to_kbs(stats.st_size),
                'creation_date': self.formating_time_kinds(stats.st_ctime),
                'modified_date': self.formating_time_kinds(stats.st_mtime),
                'last_access_date': self.formating_time_kinds(stats.st_atime),
            }

            dct_with_details[subdir.name]['metadata'] = details
            dct_with_details[subdir.name]['file_path'] = os.path.abspath(subdir)
        list_of_metadata_and_path = [dct_with_details[x] for x in dct_with_details]
        return list_of_metadata_and_path



    @staticmethod
    # get the time stamp from the file and convert it to datetime format YYYY-MM-DD HH:MM:SS in str
    def formating_time_kinds(time_statement_from_file) -> str:
        time_formated = datetime.datetime.fromtimestamp(time_statement_from_file).strftime('%Y-%m-%d %H:%M:%S')
        return time_formated

    @staticmethod
    # get the file size and convert it to size in Kbs in str
    def formating_file_size_to_kbs(file_size) -> str:
        size_as_kbs = format(file_size / 1024, ".2f")
        return size_as_kbs + " KB"