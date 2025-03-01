import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
import tkinter.scrolledtext
import ttkbootstrap
from ttkbootstrap.constants import *
import threading
import psutil
import os
import sys
import time
from functools import cache
from utils.battery_stats_scraper import BatteryStats
from utils.keyboard_input_blocker import KeyboardBlocker
from utils.tempo_file_cleaner import TempFileCleaner
from utils.onboard_malware_scanner import MalwareScanner

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class OptiGuardiumApp(ttkbootstrap.Window):
    def __init__(self):
        super().__init__()

        self.title("OptiGuardium")

        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = ttk.Frame(self, width=140)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ttk.Label(self.sidebar_frame, text="OptiGuardium", font=("Arial", 16, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_system_info_button = ttkbootstrap.Button(self.sidebar_frame, text="System Info", command=self.show_system_info)
        self.sidebar_system_info_button.grid(row=1, column=0, padx=20, pady=5)

        self.sidebar_button_2 = ttk.Button(self.sidebar_frame, text="Settings")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=5)

        self.sidebar_button_3 = ttk.Button(self.sidebar_frame, text="About")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=5)

        self.sidebar_button_4 = ttk.Button(self.sidebar_frame, text="Exit")
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=5)

        self.appearance_mode_label = ttk.Label(self.sidebar_frame, text="Appearance Mode:", font=("Arial", 12))
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(20, 0))

        self.appearance_mode_var = tk.StringVar(value="Light")

        self.appearance_mode_option_menu = ttk.OptionMenu(self.sidebar_frame, self.appearance_mode_var, "Light", "Dark", "Light", command=self.change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=6, column=0, padx=20, pady=5)

        # Main Entry and Search Button
        self.main_entry = ttk.Entry(self, width=140)
        self.main_entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # Tab View for specific features
        self.tab_control = ttk.Notebook(self)
        self.tab_1 = ttk.Frame(self.tab_control)
        self.tab_2 = ttk.Frame(self.tab_control)
        self.tab_3 = ttk.Frame(self.tab_control)
        self.tab_4 = ttk.Frame(self.tab_control)
        self.tab_5 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_1, text="OptiGuardian")
        self.tab_control.add(self.tab_2, text="OptiPerformance")
        self.tab_control.add(self.tab_3, text="OptiTempo")
        self.tab_control.add(self.tab_4, text="OptiBattery")
        self.tab_control.add(self.tab_5, text="OptiDir")
        self.tab_control.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # OptiGuardian tab information
        self.setup_malware_scanner_tab()

        # OptiPerformance tab information
        # self.setup_performance_booster_tab()

        # OptiBattery tab information
        self.setup_battery_tab()

        # OptiTempo tab information
        self.setup_temp_file_cleaner_tab()

        # OptiDir tab information
        # self.setup_directory_manager_tab()

        # ---------- Hardware Usage Frame ----------
        psutil.cpu_percent(interval=None)

        self.hardware_usage_frame = ttk.Frame(self)
        self.hardware_usage_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # System Hardware Usage Components
        self.cpu_usage_meter = ttkbootstrap.Meter(self.hardware_usage_frame, metersize=120, padding=10, amountused=0, metertype="full", subtext="CPU:", interactive=False)
        self.cpu_usage_meter.grid(row=1, column=0, padx=5, pady=5)

        self.memory_usage_meter = ttkbootstrap.Meter(self.hardware_usage_frame, metersize=120, padding=10, amountused=0, metertype="full", subtext="RAM:",  interactive=False)
        self.memory_usage_meter.grid(row=3, column=0, padx=5, pady=5)

        self.update_system_usage()


        # ---------- Disk Storage Usage ----------
        
        # Disk Labels
        # Disk Labels
        self.disk_progressbars = []
        self.disk_labels = []
        self.disk_devices = []

        for i, disk in enumerate(psutil.disk_partitions()):
            # Disks to be watched
            device_path = disk.device
            self.disk_devices.append(device_path)

            # Disk Usage Labels
            disk_label = ttkbootstrap.Label(self, text=f"{device_path}: 0.0%")
            disk_label.grid(row=i + 1, column=2, padx=10, pady=5, sticky="w")

            # Dİsk Progressbars
            disk_usage_progressbar = ttkbootstrap.Progressbar(self, orient="horizontal", length=150, mode="determinate")
            disk_usage_progressbar.grid(row=i + 1, column=1, padx=10, pady=5, sticky='w')
            
            # Append widgets to lists
            self.disk_progressbars.append(disk_usage_progressbar)
            self.disk_labels.append(disk_label)
        
        self.update_disk_info()

    
        # ---------- Features Frame ----------
        self.feature_frame = ttk.Frame(self)
        self.feature_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        
        # ---------- Keyboard Blocker ----------
        self.keyboard_blocker = KeyboardBlocker(self)
        self.keyboard_blocker_switch = ttkbootstrap.Checkbutton(
            self.feature_frame,
            bootstyle="round-toggle",
            text="Block Keyboard",
            command=self.keyboard_blocker.toggle_keyboard_input,
            variable=self.keyboard_blocker.get_block_var(),
            onvalue=True,
            offvalue=False)
        self.keyboard_blocker_switch.grid(row=0, column=0, padx=5, pady=5)


    # ---------- System Information Window ----------
    def show_system_info(self):
        """Function to display system information in a new window"""
        # self.system_info_window = SystemInfoWindow(self)
        pass


    # ---------- Malware Scanner ----------
    def setup_malware_scanner_tab(self):
        """Setting up the malware scanner tab components"""

        # Frame for logs
        malware_log_frame = ttk.LabelFrame(self.tab_1, text="Malware Scanner Log", padding=(10, 5))
        malware_log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Text widget to display the logs
        self.malware_log_text = tkinter.scrolledtext.ScrolledText(malware_log_frame, height=15, wrap="word")
        self.malware_log_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Progress Bar
        self.malware_progress_bar = ttk.Progressbar(self.tab_1, orient="horizontal", length=400, mode="determinate")
        self.malware_progress_bar.pack(pady=10)

        # Buttons for directory selection and scanning
        self.select_directory_button = ttk.Button(malware_log_frame, text="Select Directory", command=self.select_directory)
        self.select_directory_button.pack(pady=5)
        
        self.scan_button = ttk.Button(malware_log_frame, text="Start", command=self.start_scan)
        self.scan_button.pack(pady=5)

        # MalwareScanner Instance
        malware_hash_file = "data/malware_sha256_hashes.txt"
        self.scanner = MalwareScanner(malware_hash_file, self.callback_output_malware)

    def callback_output_malware(self, message):
        """Outputs messages to the malware log text widget"""
        self.malware_log_text.insert(tk.END, message + "\n")
        self.malware_log_text.update()

    def select_directory(self):
        """Opens a file dialog for the user to select a directory to scan"""
        self.scan_directory = tkinter.filedialog.askdirectory(title="Select Directory to Scan")
        if not self.scan_directory:
            self.callback_output_malware("No directory selected. Scan aborted.\n")

    def start_scan(self):
        """Starts the malware scanning process"""
        if not hasattr(self, "scan_directory") or not self.scan_directory:
            self.callback_output_malware("No directory selected. Please select a directory to scan.\n")
            return
        
        self.scanner.scan_directory(self.scan_directory, self.malware_progress_bar)


    # ---------- Temporary File Cleaner ----------
    def setup_temp_file_cleaner_tab(self):
        """Setting up the temporary file cleaner tab components"""
        # Frame for logs
        log_frame = ttk.LabelFrame(self.tab_3, text="Temporary File Cleaner Log", padding=(10, 5))
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Text widget to display the logs
        self.cleaner_log_text = tkinter.scrolledtext.ScrolledText(log_frame, height=15, wrap="word")
        self.cleaner_log_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Button for temporary file cleaner
        self.clean_temp_button = ttk.Button(self.tab_3, text="Clean TempFiles", command=self.temp_file_cleaner)
        self.clean_temp_button.pack(pady=10)

        # Label for operation result
        self.result_label = ttk.Label(log_frame, text="", font=("Arial", 10, "bold"))
        self.result_label.pack(pady=5)

    def callback_output_temp(self, message):
        """Outputs messages to the log text widget"""
        self.cleaner_log_text.insert(tk.END, message + "\n")
        self.cleaner_log_text.update()

    def temp_file_cleaner(self):
        """Calling the TempFileCleaner module to clean and logging the results"""
        self.cleaner_log_text.delete(1.0, tk.END) # Clearing the log window
        self.result_label.configure(text="", foreground="black") # Resets the result label
        
        # Operation for deleting temporary files
        try:
            temp_file_cleaner = TempFileCleaner(self.callback_output_temp)
            
            # Calling the cleaning functions with log updates
            self.callback_output_temp("Starting temporary file cleaning...\n")

            temp_file_cleaner.delete_temp_files_with_logs()
            temp_file_cleaner.delete_temp_folders_with_logs()

            self.callback_output_temp("\nCleaning completed successfully!\n")
            self.result_label.configure(text="Success: Temporary files cleaned.", foreground="green")
        except Exception as e:
            self.callback_output_temp(f"An error occured: {e}\n")
            self.result_label.configure(text="Failed: Could not clean temporary files.", foreground="red")

        self.cleaner_log_text.update()


    # ---------- Battery Stats Report ----------
    def setup_battery_tab(self):
        # Lisitng battery stats using Treeview
        columns = ("Property", "Value")
        self.battery_treeview = ttk.Treeview(self.tab_4, columns=columns, show="headings")
        self.battery_treeview.heading("Property", text="Property")
        self.battery_treeview.heading("Value", text="Value")
        self.battery_treeview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Loading battery stats
        self.load_battery_stats()

    def load_battery_stats(self):
        try:
            battery_stats = BatteryStats().parse_html_content()
            if battery_stats:
                for key, value in battery_stats.items():
                    self.battery_treeview.insert("", "end", values=(key, value))
            else:
                self.battery_treeview.insert("", "end", values=("Error", "N/A"))
        except Exception as e:
            self.battery_treeview.insert("", "end", values=("Error", str(e)))

    def update_system_usage(self):
        cpu_usage = psutil.cpu_percent(interval=None)
        memory_usage = psutil.virtual_memory().percent

        self.cpu_usage_meter.configure(amountused=cpu_usage)
        self.memory_usage_meter.configure(amountused=memory_usage)
        
        # Update the labels with the new information
        self.cpu_usage_meter.configure(subtext=f"CPU (%):")
        self.memory_usage_meter.configure(subtext=f"RAM (%):")
        # Get system usage information
        cpu_usage = psutil.cpu_percent(interval=0)
        memory_usage = psutil.virtual_memory().percent

        # Schedule the next update after 1 second
        self.after(1000, self.update_system_usage)

    
    def update_disk_info(self):
        # Updating the information of each disk every second
            for i, (disk_label, disk_progressbar, device_path) in enumerate(zip(self.disk_labels, self.disk_progressbars, self.disk_devices)):
                # Getting disk usage value
                if not device_path.endswith(':\\'):
                    device_path += ':\\'
                
                try:
                    disk_usage = psutil.disk_usage(device_path)
                    usage_percent = disk_usage.percent
                except PermissionError:
                    usage_perccent = 0

                # Update label
                disk_label.configure(text=f"{device_path}: {usage_percent:.2f}%")

                # Update progress bar
                disk_progressbar.configure(value=usage_percent)

            self.after(1000, self.update_disk_info)

    def update_network_info(self):
        pass

    def change_appearance_mode_event(self, new_value):
        if new_value == "Light":
            self.style.theme_use("litera")
        elif new_value == "Dark":
            self.style.theme_use("darkly")
        
        



if __name__ == "__main__":
    app = OptiGuardiumApp()
    app.mainloop()


        
