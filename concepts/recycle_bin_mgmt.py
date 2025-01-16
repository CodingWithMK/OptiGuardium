import ctypes.wintypes
import customtkinter
import winshell
from tkinter import messagebox
import ctypes

# Tkinter bileşenlerini import etmek zorunda değiliz; CustomTkinter'ı kullanacağız.

customtkinter.set_appearance_mode('system')
customtkinter.set_default_color_theme('green')

class RecycleBin(customtkinter.CTk):
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

if __name__ == '__main__':
    app = RecycleBin()
    app.mainloop()
