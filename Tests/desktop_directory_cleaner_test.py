import os
import shutil
import datetime

class DesktopDirectoryCleanerTest:
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

    def move_file_to_documents_directory(self):
        is_file = self.check_for_file_on_desktop()
        print(is_file)
        for file in is_file:
            shutil.move(file, self.documents_directory)
            print(f"File moved to Documents dir successfully: {file}")

    def move_folder_to_documents_directory(self):
        is_folder = self.check_for_folder_on_desktop()
        print(is_folder)
        for folder in is_folder:
            shutil.move(folder, self.documents_directory)
            print(f"File moved to Documents dir successfully: {folder}")

    def run(self):
        self.check_for_file_on_desktop()
        self.check_for_folder_on_desktop()
        self.move_file_to_documents_directory()
        self.move_folder_to_documents_directory()
        print("Files in Desktop directory cleaned successfully.")

        
if __name__ == "__main__":
    downloads_directory_cleaner = DesktopDirectoryCleanerTest()
    downloads_directory_cleaner.run()