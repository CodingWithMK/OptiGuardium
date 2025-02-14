"""
This script is to organize and clean your desktop on your system. The files an d folders on your desktop get moved
to the documents directory on your system by their extensions.
Every run of the script will create a folder for each category with the current date and the name of the category.
After that, the program will move the files to the corresponding folder.
"""

import os
import shutil
import datetime

class DesktopDirectoryOrganizer:
    def __init__(self):
        
        self.documents_directory = os.path.expanduser("~/Documents")
        self.desktop_directory = os.path.expanduser("~/Desktop")

        self.extensions = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
            "Videos": [".mp4", ".mov", ".avi", ".mkv"],
            "Audios": [".mp3", ".wav", ".ogg", ".m4a"],
            "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".csv"],
            "Compressed": [".zip", ".rar", ".tar", ".gz", ".7z", ".torrent"],
            "Fonts": [".ttf", ".otf"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".json", ".go", ".php", ".rust", ".ruby", ".scala", ".swift", ".cs", ".kt"],
        }

    def generate_category_folders(self):
        for categories, extensions in self.extensions.items():
            category_folder = os.path.join(self.documents_directory, categories)
            if not os.path.exists(category_folder):
                os.makedirs(category_folder)

    def generate_date_folders(self):
        categories = self.extensions.keys()
        print(f"Categories: {categories}")
        date_folders = {}
        for category in categories:
            print(f"Processing: {category}")
            timestamp = datetime.datetime.now().strftime(f"{category} %Y-%m-%d_%H-%M-%S")
            # Generate folders with current date and category name
            category_date_folder = os.path.join(
                self.documents_directory,
                category,
                f"{timestamp}"
            )
            if not os.path.exists(category_date_folder):
                os.makedirs(category_date_folder)
                print(f"Generating: {category_date_folder}")
            else:
                print(f"Folder already exists: {category_date_folder}")

            date_folders[category] = category_date_folder # Storing date folders in the set

        return date_folders

    def check_for_file_on_desktop(self) -> list:
        desktop_files = []
        desktop_files_dir = os.listdir(self.desktop_directory)
        for file in desktop_files_dir:
            file_path = os.path.join(self.desktop_directory, file)
            for extensions in self.extensions.values():
                if os.path.isfile(file_path) and file.endswith(tuple(extensions)):
                    desktop_files.append(file_path)
                    print(f"File found on Desktop: {file}")
        return desktop_files
                
    def check_for_folder_on_desktop(self) -> list:
        desktop_folders = []
        desktop_folders_dir = os.listdir(self.desktop_directory)
        for folder in desktop_folders_dir:
            folder_path = os.path.join(self.desktop_directory, folder)
            if os.path.isdir(folder_path):
                desktop_folders.append(folder_path)
                print(f"Folder found on Desktop: {folder}")
        return desktop_folders

    def move_file_to_documents_directory(self, date_folder):
        is_file = self.check_for_file_on_desktop()
        print(is_file)
        for file in is_file:
            file_lower = file.lower()
            for category, extension in self.extensions.items():
                if file_lower.endswith(tuple(extension)):
                    category_date_folder = date_folder.get(category)
                    if category_date_folder:
                        shutil.move(file, category_date_folder)
                        print(f"Moved {file} to {category_date_folder}")
                        moved = True
                        break
            if not moved:
                print(f"File {file} not moved to any category folder.")
        print("Files moved to date folders in docs directory successfully.")

    def move_folder_to_documents_directory(self):
        is_folder = self.check_for_folder_on_desktop()
        print(is_folder)
        for folder in is_folder:
            shutil.move(folder, self.documents_directory)
            print(f"File moved to Documents dir successfully: {folder}")

    def run(self):
        self.generate_category_folders()
        date_folder = self.generate_date_folders()
        self.move_file_to_documents_directory(date_folder)
        self.move_folder_to_documents_directory()
        print("Files on Desktop cleaned and moved to Docs directory successfully.")

        
if __name__ == "__main__":
    downloads_directory_organizer = DesktopDirectoryOrganizer()
    downloads_directory_organizer.run()