from os import lstat

from dotenv import load_dotenv, find_dotenv
import datetime
import pathlib
import pprint
import json
import time
import os


load_dotenv(find_dotenv())

class Reader:

    def __init__(self):
        self.MainDirPath = os.getenv('MAIN_DATA_PATH')

    def get_list_of_details(self):
        lst_of_details = self.loop_through_path_and_create_dct_of_details()
        return lst_of_details

    def loop_through_path_and_create_dct_of_details(self):
        if self.MainDirPath is None:
            raise Exception('Path Not Exist')

        path = pathlib.Path(self.MainDirPath)
        dct_with_details = {}

        for subdir in path.iterdir():
            stats = os.stat(subdir)

            dct_with_details[subdir.name] = {}

            details = {
                'File Name': subdir.name,
                'Size (KB)': self.formating_file_size_to_kbs(stats.st_size),
                'Creation Date': self.formating_time_kinds(stats.st_ctime),
                'Modified Date': self.formating_time_kinds(stats.st_mtime),
                'Last Access Date': self.formating_time_kinds(stats.st_atime),
            }

            dct_with_details[subdir.name]['Metadata'] = details
            dct_with_details[subdir.name]['File Path'] = os.path.abspath(subdir)
        list_of_metadata_and_path = [x.value for x in dct_with_details]
        return list_of_metadata_and_path


    @staticmethod
    def formating_time_kinds(time_statement_from_file):
        time_formated = datetime.datetime.fromtimestamp(time_statement_from_file).strftime('%Y-%m-%d %H:%M:%S')
        return time_formated

    @staticmethod
    def formating_file_size_to_kbs(file_size):
        size_as_kbs = format(file_size / 1024, ".2f")
        return size_as_kbs + " KB"