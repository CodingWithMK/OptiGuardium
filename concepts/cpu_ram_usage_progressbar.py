import customtkinter
import psutil
import time

customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')

class SystemUsageMonitorProgressBar(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('CPU and RAM Usage Monitor')

        # CPU Usage Progress Bar
        self.cpu_usage_label = customtkinter.CTkLabel(self, text='CPU Usage:')
        self.cpu_usage_label.pack(pady=10)
        self.cpu_usage_progressbar = customtkinter.CTkProgressBar(self, orientation='horizontal')
        self.cpu_usage_progressbar.pack(pady=10)

        # RAM Usage Progress Bar
        self.ram_usage_label = customtkinter.CTkLabel(self, text='RAM Usage:')
        self.ram_usage_label.pack(pady=10)
        self.ram_usage_progressbar = customtkinter.CTkProgressBar(self, orientation='horizontal')
        self.ram_usage_progressbar.pack(pady=10)

        self.update_progressbars()

    def update_progressbars(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent

        self.cpu_usage_progressbar.set(cpu_usage / 100)
        self.ram_usage_progressbar.set(ram_usage / 100)

        # Updating CPU Percentage Display
        self.cpu_usage_label.configure(text=f"CPU: {cpu_usage:.2f}%")
        # Updating RAM Percentage Display
        self.ram_usage_label.configure(text=f"RAM: {ram_usage:.2f}%")

        self.after(1000, self.update_progressbars)

if __name__ == "__main__":
    app = SystemUsageMonitorProgressBar()
    app.mainloop()