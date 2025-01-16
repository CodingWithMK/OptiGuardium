import tkinter as tk
from tkinter import ttk
import customtkinter
import psutil
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotly.express as pltx


class SystemUsageMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("System Usage Monitor")
        self.geometry("640x480")

        self.style = ttk.Style(self)
        self.tk.call("source", "themes/forest-ttk-theme/forest-light.tcl")
        self.tk.call("source", "themes/forest-ttk-theme/forest-dark.tcl")
        self.style.theme_use("forest-dark")

        self.cpu_usage_label = tk.Label(self, text="CPU Usage: 0%", font=("Arial", 12))
        self.cpu_usage_label.grid(row=0, column=0, pady=5)
        self.cpu_usage_progressbar = customtkinter.CTkProgressBar(self, orientation="horizontal")
        self.cpu_usage_progressbar.grid(row=1, column=0, padx=5, pady=5)

        self.memory_usage_label = tk.Label(self, text="RAM Usage: 0%", font=("Arial", 12))
        self.memory_usage_label.grid(row=2, column=0, pady=5)
        self.memory_usage_progressbar = customtkinter.CTkProgressBar(self, orientation="horizontal")
        self.memory_usage_progressbar.grid(row=3, column=0, padx=5, pady=5)

        self.update_system_usage()

    def update_system_usage(self):
        # Get system usage information
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent

        self.cpu_usage_progressbar.set(cpu_usage / 100)
        self.memory_usage_progressbar.set(memory_usage / 100)

        # Update the labels with the new information
        self.cpu_usage_label.config(text=f"CPU Usage: {cpu_usage}%")
        self.memory_usage_label.config(text=f"RAM Usage: {memory_usage}%")

        # Schedule the next update after 1 second
        self.after(1000, self.update_system_usage)

if __name__ == "__main__":
    app = SystemUsageMonitor()
    app.mainloop()