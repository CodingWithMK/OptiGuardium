import customtkinter
import fitz
import os
import io
from PIL import Image, ImageTk
import cv2
import winshell
import ctypes
import ctypes.wintypes



class FileViewer(customtkinter.CTk):
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
    app = FileViewer()
    app.mainloop()