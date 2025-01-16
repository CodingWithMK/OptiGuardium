import os
import sys
import re
import shutil
import time


class TempFileCleaner():

    def __init__(self):
        self.temp_folder_path = os.path.expanduser('~\\AppData\\Local\\Temp')
        self.temp_file_pattern = re.compile(r'^(?=.*[a-z])(?=.*[0-9]).*$')
        self.days_old = 1 # Defines the days to delete the files (by default 1 day)

    def is_file_old(self, filepath):
        file_time = os.path.getmtime(filepath)
        return (time.time() - file_time) / (24 * 3600 >= self.days_old)

    def delete_temp_files(self):
        for root, dirs, files in os.walk(self.temp_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if self.temp_file_pattern.match(file) and self.is_file_old(file_path):
                    try:
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    except PermissionError:
                        print(f"Failed to delete file: {file_path}. Permission denied.")
                    except Exception as error:
                        print(f"Failed to delete file: {file_path}. Error: {error}")

    def delete_temp_folders(self):
        for root, dirs, files in os.walk(self.temp_folder_path):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if self.temp_file_pattern.match(dir):
                    try:
                    # os.rmdir(os.path.join(root, dir))
                        shutil.rmtree(os.path.join(root, dir))
                        print(f"Deleted folder: {dir_path}")
                    except PermissionError:
                        print(f"Failed to delete folder: {dir_path}. Permission denied.")
                    except Exception as error:
                        print(f"Failed to delete folder: {dir_path}. Error: {error}")

    def delete_temp_data(self):
        self.delete_temp_files()
        self.delete_temp_folders()

    def main(self):
        self.delete_temp_data()

        print("All temp files and folders deleted successfully.")

        sys.exit(0)

if __name__ == "__main__":
    app = TempFileCleaner()
    app.main()