import os
import sys
import re
import shutil
import time


class TempFileCleaner():

    def __init__(self, callback_output_temp):
        self.temp_folder_path = os.path.expanduser('~\\AppData\\Local\\Temp')
        self.temp_file_pattern = re.compile(r'^(?=.*[a-z])(?=.*[0-9]).*$')
        self.days_old = 1 # Defines the days to delete the files (by default 1 day)
        self.callback_output_temp = callback_output_temp

    def is_file_old(self, filepath):
        file_time = os.path.getmtime(filepath)
        return (time.time() - file_time) / (24 * 3600 >= self.days_old)

    def delete_temp_files_with_logs(self):
        for root, dirs, files in os.walk(self.temp_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if self.temp_file_pattern.match(file) and self.is_file_old(file_path):
                    try:
                        os.remove(file_path)
                        self.callback_output_temp(f"Deleted file: {file_path}")
                    except PermissionError:
                        self.callback_output_temp(f"Failed to delete file: {file_path}. Permission denied.")
                    except Exception as error:
                        self.callback_output_temp(f"Failed to delete file: {file_path}. Error: {error}")

    def delete_temp_folders_with_logs(self):
        for root, dirs, files in os.walk(self.temp_folder_path):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if self.temp_file_pattern.match(dir):
                    try:
                        # os.rmdir(os.path.join(root, dir))
                        shutil.rmtree(os.path.join(root, dir))
                        self.callback_output_temp(f"Deleted folder: {dir_path}")
                    except PermissionError:
                        self.callback_output_temp(f"Failed to delete folder: {dir_path}. Permission denied.")
                    except Exception as error:
                        self.callback_output_temp(f"Failed to delete folder: {dir_path}. Error: {error}")

    def delete_temp_data(self):
        self.delete_temp_files_with_logs()
        self.delete_temp_folders_with_logs()

    def delete(self):
        try:
            self.delete_temp_data()
            self.callback_output_temp("All temp files and folders deleted successfully.")
        except Exception as e:
            self.callback_output_temp(f"An error occurred while deleting temporary files: {e}")

        

if __name__ == "__main__":
    TempFileCleaner()