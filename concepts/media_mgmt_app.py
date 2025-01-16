import customtkinter
import winshell
import ctypes
import os
from PIL import Image, ImageTk
import ctypes.wintypes
import io
import fitz
from tkinter import messagebox
import cv2


customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('green')

class MediaManagementApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('System Management')
        self.geometry('1100x580')

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Media App", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.file_viewer_button = customtkinter.CTkButton(self, text="Open File Viewer", command=FileViewer)
        self.file_viewer_button.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.recycle_bin_button = customtkinter.CTkButton(self, text="Open Recycle Bin", command=RecycleBin)
        self.recycle_bin_button.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)





class RecycleBin(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title('Recycle Bin')
        self.geometry('640x480')

        self.recycle_bin_label = customtkinter.CTkLabel(self, text='Recycle Bin Content')
        self.recycle_bin_label.grid(column=0, row=0, pady=10)

        self.item_searchbar = customtkinter.CTkEntry(self, width=400, corner_radius=16, border_color='orange', placeholder_text="Search for item...")
        self.item_searchbar.grid(row=1, column=0, padx=10, pady=10)

        self.item_searchbar.bind('<KeyRelease>', self.search_items)

        # CTkScrollableFrame oluşturma
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, width=600, height=300, border_color='orange', scrollbar_button_hover_color='white')
        self.scrollable_frame.grid(column=0, row=2, padx=10, pady=10, sticky='nsew')

        self.empty_button = customtkinter.CTkButton(self, text='Empty',corner_radius=16, border_color='red', command=self.empty_recycle_bin)
        self.empty_button.grid(column=0, row=3, pady=10)

        # Geri dönüşüm kutusu öğelerini listeleme
        self.original_items = [] # list of original recycle bin items
        self.list_recycle_bin_items()
        

    def list_recycle_bin_items(self):
        # Geri dönüşüm kutusundaki tüm öğeleri alın
        recycle_bin_items = list(winshell.recycle_bin())
        self.original_items = recycle_bin_items # Storing original items

        # Updating recycle bin items
        self.update_listbox(self.original_items)

    def update_listbox(self, items):
        # ScrollableFrame içindeki mevcut tüm widget'ları temizleyin
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Her öğe için CTkLabel ekleyin
        for index, item in enumerate(items):
            try:
                filename = item.original_filename()
                if filename:
                    label = customtkinter.CTkLabel(self.scrollable_frame, text=f'Item {index + 1}: {filename}')
                    label.pack(pady=5, padx=10, anchor='w')  # Sola hizalama
                    label.bind("<Double-Button-1>", lambda event, file=item: self.ask_action_on_file(file))
            except Exception as e:
                print(f"Error processing item {index}: {e}")

    def search_items(self, event):
        # Getting input from searchbar
        search_query = self.item_searchbar.get().strip().lower() # Getting searchbar input and convert to lower

        # Listing original items if search bar is empty
        if search_query == '':
            self.update_listbox(self.original_items)
            return

        # Filtering same items with search input
        filtered_items = [item for item in self.original_items if search_query in item.original_filename().lower()] 

        # Updating filtered items
        self.update_listbox(filtered_items)

    def empty_recycle_bin(self):
        # Geri dönüşüm kutusundaki tüm öğeleri silin
        empty_bin = winshell.recycle_bin().empty(confirm=True, show_progress=True, sound=True)
        if empty_bin:
            print("Recycle Bin successfully emptied.")
        else:
            print("Process canceled.")

        # Öğeleri güncelle
        self.list_recycle_bin_items()

    
    def ask_action_on_file(self, file):
        filename = file.original_filename()
        action_window = customtkinter.CTkToplevel(self)
        action_window.title(filename)
        action_window.geometry("300x150")

        file_action_label = customtkinter.CTkLabel(action_window, text=f"What to do with {filename}?")
        file_action_label.pack(pady=10)

        restore_button = customtkinter.CTkButton(action_window, text="Restore", command=lambda: self.restore_file(file, action_window))
        restore_button.pack(pady=5)

        delete_button = customtkinter.CTkButton(action_window, text="Delete", command=lambda: self.delete_file(file, action_window))
        delete_button.pack(pady=5)


    def restore_file(self, file, window):
        try:
            file_path = file.filename()
            original_path = file.original_filename()
            # file.restore() # Restoring file using winshell function

            if self.restore_file_to_original_location(file_path, original_path):
                messagebox.showinfo("Success", f"File {file.original_filename()} restored successfully.")
            else:
                messagebox.showerror("Error", f"Failed to restore {file.original_filename()}. Error: {e}")
            
            window.destroy()
            self.list_recycle_bin_items() # Updating recycle bin list after restoring file
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore {file.original_filename()}. Error: {e}")

    def delete_file(self, file, window):
        try:
            file_path = file.filename()
            if self.delete_file_permanently(file_path):
                # file.delete() # Deleting file using winshell function
                messagebox.showinfo("Success", f"File {file.original_filename()} deleted successfully.")
            else:
                messagebox.showerror("Error", f"Failed to delete {file.original_filename()}. Error: {e}")

            window.destroy()
            self.list_recycle_bin_items() # Updating recycle bin list after deleting file
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete {file.original_filename()}. Error: {e}")

        

    def restore_file_to_original_location(self, file_path, original_path):
        sh_file_operation = ctypes.windll.shell32.SHFileOperationW
        FO_MOVE = 0x0001
        FOF_SILENT = 0x0004
        FOF_NOCONFIRMATION = 0x0010

        op = SHFILEOPSTRUCT()
        op.wFunc = FO_MOVE
        op.pFrom = f"{file_path}\0"
        op.pTo = f"{original_path}\0"
        op.fFlags = FOF_NOCONFIRMATION
        

        result = sh_file_operation(ctypes.byref(op))

        return result == 0 # Returning '0' if successful
    

    def delete_file_permanently(self, file_path):
        sh_file_operation = ctypes.windll.shell32.SHFileOperationW
        FO_DELETE = 0x0003
        FOF_SILENT = 0x0004
        FOF_NOCONFIRMATION = 0x0010

        op = SHFILEOPSTRUCT()
        op.wFunc = FO_DELETE
        op.pFrom = f"{file_path}\0"
        op.pTo = None
        op.fFlags = FOF_NOCONFIRMATION

        result = sh_file_operation(ctypes.byref(op))

        return result == 0 # Returning '0' if successful

class SHFILEOPSTRUCT(ctypes.Structure):
    _fields_ = [
        ('hwnd', ctypes.c_void_p),
        ('wFunc', ctypes.c_uint),
        ('pFrom', ctypes.c_wchar_p),
        ('pTo', ctypes.c_wchar_p),
        ('fFlags', ctypes.c_uint),
        ('fAnyOperationsAborted', ctypes.c_bool),
        ('hNameMappings', ctypes.c_void_p),
        ('lpszProgressTitle', ctypes.c_wchar_p)
    ]




class FileViewer(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("File Viewer")
        self.geometry("200x100")
    
        self.explorer_button = customtkinter.CTkButton(self, text="Open Explorer", corner_radius=12, border_color='yellow', command=self.open_win_explorer)
        self.explorer_button.pack(pady=10)


    def open_win_explorer(self):
        file_path = customtkinter.filedialog.askopenfilename(initialdir='C:/Users/%s',
                                                                      filetypes=[("All Files", "*.*"),
                                                                                 ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
                                                                                 ("PDF Files", "*.pdf"),
                                                                                 ("Video Files", "*.mp4;*.mkv;*.avi;*.mov")])

        if file_path is not None:
            self.view_file(file_path)

    def view_file(self, file_path):
        # image files
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            self.view_image(file_path)

        # pdf files
        elif file_path.lower().endswith('.pdf'):
            self.view_pdf(file_path)

        # video files
        elif file_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
            self.view_video(file_path)
        
        elif not file_path:
            print("No file selected. Process canceled.")

        else:
            print(f"Unsupported file type: {file_path}")


    def view_image(self, file_path):
        img_viewer = customtkinter.CTkToplevel(self)
        img_viewer.title("Image Viewer")
        img_viewer.geometry("800x600")

        image = Image.open(file_path)
        image = image.resize((800, 600), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label = customtkinter.CTkLabel(img_viewer, image=photo)
        label.image = photo
        label.pack()


    def view_pdf(self, file_path):
        pdf_viewer = customtkinter.CTkToplevel(self)
        pdf_viewer.title("PDF Viewer")
        pdf_viewer.geometry("800x600")

        pdf_document = fitz.open(file_path)
        page = pdf_document.load_page(0)

        pix = page.get_pixmap()
        img_data = io.BytesIO(pix.tobytes())
        img = Image.open(img_data)

        img = img.resize((800, 600), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        label = customtkinter.CTkLabel(pdf_viewer, image=photo)
        label.image = photo
        label.pack()


    def view_video(self, file_path):
        video_viewer = customtkinter.CTkToplevel(self)
        video_viewer.title("Video Viewer")
        video_viewer.geometry("800x600")

        video = cv2.VideoCapture(file_path)

        def play_video():
            ret, frame = video.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img_tk = ImageTk.PhotoImage(image=img)
                
                if not hasattr(play_video, 'label'):
                    play_video.label = customtkinter.CTkLabel(video_viewer, image=img_tk)
                    play_video.label.image = img_tk
                    play_video.label.pack()

                else:
                    play_video.label.configure(image=img_tk)
                    play_video.label.image = img_tk
            
        
                video_viewer.after(20, play_video)
            else:
                video.release()

        video_viewer.after(0, play_video)        
        video_viewer.protocol("WM_DELETE_WINDOW", lambda: (video.release(), cv2.destroyAllWindows(), video_viewer.destroy()))

if __name__ == '__main__':
    app = MediaManagementApp()
    app.mainloop()
