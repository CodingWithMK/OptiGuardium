'''
This script organizes the files in the Downloads folder into different categories based on their file extensions.
The script creates folders for each category and moves the files to the respective category folders.
The script also creates date folders inside each category folder to organize files based on the download date.
'''

import os
import shutil
import datetime


class DownloadsOrganizer:
    def __init__(self):
        self.downloads_folder = os.path.expanduser("D:\\~\\Downloads")
        self.extensions = {
            "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
            "Videos": ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv'],
            "Documents": ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
            "Audio": ['.mp3', '.wav', '.ogg', '.flac'],
            "Archives": ['.zip', '.rar', '.7z', '.tar', '.gz', '.dmg'],
            "Executables": ['.exe', '.msi'],
            "Code": ['.py', '.java', '.cpp', '.html', '.css', '.js'],
            "Compressed": ['.zip', '.rar', '.7z', '.tar', '.gz'],
            "Fonts": ['.ttf', '.otf', '.fon'],
        }

    def create_category_folders(self):
        for category in self.extensions.keys():
            os.makedirs(os.path.join(self.downloads_folder, category), exist_ok=True)

    def create_date_folders(self):
        categories = tuple(self.extensions.keys())
        for category in categories:
            date_folder = os.path.join(self.downloads_folder, category, datetime.datetime.now().strftime("%Y-%m-%d"))
            date_folders = os.makedirs(date_folder, exist_ok=True)
            return date_folders

    def move_files_to_date_folders(self, date_folder):
        date_folder = self.create_date_folders()
        for category, extensions in self.extensions.items():
            for filename in os.listdir(os.path.join(self.downloads_folder, category)):
                file_path = os.path.join(self.downloads_folder, category, filename)
                if os.path.isfile(file_path) and os.path.splitext(file_path)[1] in extensions:
                    shutil.move(file_path, date_folder)

    def move_date_folders_to_category_folders(self):
        for category in self.extensions.keys():
            for date_folder in os.listdir(os.path.join(self.downloads_folder, category)):
                date_folder_path = os.path.join(self.downloads_folder, category, date_folder)
                if os.path.isdir(date_folder_path):
                    for filename in os.listdir(date_folder_path):
                        file_path = os.path.join(date_folder_path, filename)
                        if os.path.isfile(file_path):
                            shutil.move(file_path, os.path.join(self.downloads_folder, category))

    def run(self):
        self.create_category_folders()
        self.create_date_folders()
        self.move_files_to_date_folders(date_folders)
        self.move_date_folders_to_category_folders()

if __name__ == "__main__":
    organizer = DownloadsOrganizer()
    organizer.run()

