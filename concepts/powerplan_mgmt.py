import subprocess
import customtkinter as ctk
from tkinter import messagebox

def is_power_mode_available(scheme_guid):
    """Check if the specified power mode is already available."""
    try:
        result = subprocess.check_output(["powercfg", "/LIST"], shell=False, text=True)
        return scheme_guid in result
    except Exception as e:
        messagebox.showerror("Error", f"Failed to check power modes: {e}")
        return False

def get_ultimate_performance_guid():
    """Retrieve the GUID of the existing Ultimate Performance plan, if available."""
    try:
        result = subprocess.check_output(["powercfg", "/LIST"], shell=False, text=True)
        for line in result.splitlines():
            if "Ultimate Performance" in line:
                return line.split()[3]  # Extract the GUID from the line
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve Ultimate Performance GUID: {e}")
    return None

def add_ultimate_performance():
    """Add Ultimate Performance mode to the system."""
    try:
        result = subprocess.check_output([
            "powercfg", "-duplicatescheme", "e9a42b02-d5df-448d-aa00-03f14749eb61"
        ], shell=False, text=True)
        new_guid = get_ultimate_performance_guid()
        if new_guid:
            return new_guid
        else:
            raise subprocess.SubprocessError("Failed to retrieve new GUID after adding Ultimate Performance mode.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add Ultimate Performance mode: {e}")
        return None

def enable_ultimate_performance():
    """Enable the Ultimate Performance mode."""
    scheme_guid = get_ultimate_performance_guid()

    if not scheme_guid:
        scheme_guid = add_ultimate_performance()
        if not scheme_guid:
            return False

    try:
        subprocess.run(["powercfg", "/SETACTIVE", scheme_guid], shell=False, check=True)
        return True
    except subprocess.SubprocessError:
        messagebox.showerror("Error", "Failed to activate Ultimate Performance mode.")
        return False

def disable_ultimate_performance():
    """Disable the Ultimate Performance mode and switch to Balanced mode."""
    balanced_scheme_guid = "381b4222-f694-41f0-9685-ff5bb260df2e"  # GUID for Balanced plan
    try:
        subprocess.run(["powercfg", "/SETACTIVE", balanced_scheme_guid], shell=False, check=True)
        return True
    except subprocess.SubprocessError:
        messagebox.showerror("Error", "Failed to switch to Balanced mode.")
        return False

class PowerModeSwitcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Performance Mode Switch")

        self.create_widgets()
        self.check_initial_state()

    def create_widgets(self):
        """Create the main UI components."""
        self.label = ctk.CTkLabel(self.root, text="Ultimate Performance Mode:", font=("Arial", 14))
        self.label.pack(pady=10)

        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(
            self.root,
            text="Enable",
            variable=self.switch_var,
            onvalue="on",
            offvalue="off",
            command=self.toggle_performance_mode
        )
        self.switch.pack(pady=10)

    def check_initial_state(self):
        """Check if the Ultimate Performance Mode is already active."""
        scheme_guid = get_ultimate_performance_guid()
        if scheme_guid and is_power_mode_available(scheme_guid):
            self.switch_var.set("on")

    def toggle_performance_mode(self):
        """Enable or disable the Ultimate Performance Mode based on the switch state."""
        if self.switch_var.get() == "on":
            if enable_ultimate_performance():
                messagebox.showinfo("Success", "Ultimate Performance Mode enabled.")
            else:
                self.switch_var.set("off")
        else:
            if disable_ultimate_performance():
                messagebox.showinfo("Success", "Ultimate Performance Mode disabled. Switched to Balanced mode.")
            else:
                self.switch_var.set("on")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = PowerModeSwitcher(root)
    root.mainloop()
