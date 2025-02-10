"""
This script is to organize the downloads directory in your system by their extensions.
Every run of the script will create a folder for each category with the current date and the name of the category.
After that, the program will move the files to the corresponding folder.
"""

import os
import shutil
import datetime

class DownloadsDirectoryOrganizer:
    def __init__(self):
        
        self.downloads_directory = os.path.expanduser("~/Downloads")

        self.extensions = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
            "Videos": [".mp4", ".mov", ".avi", ".mkv"],
            "Audios": [".mp3", ".wav", ".ogg", ".m4a"],
            "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".csv"],
            "Executables": [".exe", ".msi", ".pkg"],
            "Compressed": [".zip", ".rar", ".tar", ".gz", ".7z", ".torrent"],
            "Fonts": [".ttf", ".otf"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".json", ".go", ".php", ".rust", ".ruby", ".scala", ".swift", ".cs", ".kt"],
        }

    def generate_category_folders(self):
        for categories, extensions in self.extensions.items():
            category_folder = os.path.join(self.downloads_directory, categories)
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
                self.downloads_directory,
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
        
    def move_files_to_date_folders(self, date_folder):
        downloads_directory = self.downloads_directory
        # Checking category for each file while listing all files is more efficient
        for file in os.listdir(downloads_directory):
            file_path = os.path.join(downloads_directory, file)
            if os.path.isfile(file_path):
                # Determine category for each file
                file_lower = file.lower()
                moved = False # Checking if file moved or not
                for category, extensions in self.extensions.items():
                    if file_lower.endswith(tuple(extensions)):
                        # Move file to corresponding category folder
                        category_date_folder = date_folder.get(category)
                        if category_date_folder:
                            shutil.move(file_path, category_date_folder)
                            print(f"Moved {file} to {category_date_folder}")
                            moved = True
                            break
                if not moved:
                    print(f"File {file} not moved to any category folder.")
        print("Files moved to date folders successfully.")

    def run(self):
        self.generate_category_folders()
        date_folder = self.generate_date_folders()
        self.move_files_to_date_folders(date_folder)
        print("Files in Downloads directory organized successfully.")

        
if __name__ == "__main__":
    downloads_directory_organizer = DownloadsDirectoryOrganizer()
    downloads_directory_organizer.run()