import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import threading
import psutil
import os
import sys
import sv_ttk

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class OptiGuardiumApp(tk.Tk()):
    def __init__(self):
        super.__init__()

        self.title("OptiGuardium")

        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")

        self.style = ttk.Style(self)
        self.tk.call("source", "themes/forest-ttk-theme/forest-light.tcl")
        self.tk.call("source", "themes/forest-ttk-theme/forest-dark.tcl")
        self.style.theme_use("forest-dark")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = tk.Frame(self, width=140)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = tk.Label(self.sidebar_frame, text="OptiGuardium", font=("Arial", 16, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = tk.Button(self.sidebar_frame, text="Dashboard", font=("Arial", 14))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=5)

        self.sidebar_button_2 = tk.Button(self.sidebar_frame, text="Settings", font=("Arial", 14))
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=5)

        self.sidebar_button_3 = tk.Button(self.sidebar_frame, text="About", font=("Arial", 14))
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=5)

        self.sidebar_button_4 = tk.Button(self.sidebar_frame, text="Exit", font=("Arial", 14))
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=5)

        self.appearance_mode_label = tk.Label(self.sidebar_frame, text="Appearance Mode:", font=("Arial", 12))
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(20, 0))

        self.appearance_mode_option_menu = ttk.OptionMenu(self.sidebar_frame, tk.StringVar(), "Light", "Dark", "System")
        self.appearance_mode_option_menu.grid(row=6, column=0, padx=20, pady=5)

        self.scaling_label = tk.Label(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        self.scaling_option_menu = ttk.OptionMenu(self.sidebar_frame, tk.StringVar(), "125%", "100%", "75%", "50%", self.change_scaling_event)
        self.scaling_option_menu.grid(row=8, column=0, padx=20, pady=(10, 20))



        
