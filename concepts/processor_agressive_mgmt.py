import subprocess
import customtkinter as ctk
from tkinter import messagebox

def set_processor_boost_mode(value):
    """Set the Processor Performance Boost Mode to the specified value."""
    try:
        # Önce gizli güç ayarlarını ortaya çıkaralım
        subprocess.run([
            "powercfg", "-attributes",
            "SUB_PROCESSOR", "PROCTHROTTLEMIN", "-ATTRIB_HIDE"
        ], shell=False, check=True)
        # Ayarı değiştir
        subprocess.run([
            "powercfg", "-setacvalueindex",
            "SCHEME_CURRENT", "SUB_PROCESSOR",
            "be337238-0d82-4146-a960-4f3749d470c7", str(value)
        ], shell=False, check=True)
        # Değişiklikleri uygula
        subprocess.run(["powercfg", "-S", "SCHEME_CURRENT"], shell=False, check=True)
        return True
    except subprocess.SubprocessError as e:
        messagebox.showerror("Error", f"Failed to set Processor Performance Boost Mode: {e}")
        return False

def get_processor_boost_mode():
    """Get the current Processor Performance Boost Mode value."""
    try:
        result = subprocess.check_output([
            "powercfg", "-q",
            "SCHEME_CURRENT", "SUB_PROCESSOR",
            "be337238-0d82-4146-a960-4f3749d470c7"
        ], shell=False, text=True)
        # Çıktıdan mevcut değeri ayıklayalım
        lines = result.splitlines()
        for i in range(len(lines)):
            if "Current AC Power Setting Index" in lines[i]:
                # Değer ondalık veya hex olabilir
                value_str = lines[i].split(":")[-1].strip()
                value = int(value_str, 0)  # Otomatik taban algılama
                return value
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get Processor Performance Boost Mode: {e}")
        return None

class PowerModeSwitcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Performance Boost Mode Switch")

        self.create_widgets()
        self.check_initial_state()

    def create_widgets(self):
        """Create the main UI components."""
        self.label = ctk.CTkLabel(self.root, text="Processor Performance Boost Mode:", font=("Arial", 14))
        self.label.pack(pady=10)

        # Seçenekler
        options = [
            ("Disabled", 0),
            ("Enabled", 1),
            ("Aggressive", 2),
            ("Efficient Enabled", 3),
            ("Efficient Aggressive", 4),
            ("Aggressive at Guaranteed", 5),
            ("Efficient Aggressive at Guaranteed", 127)
        ]

        self.boost_mode_var = ctk.StringVar()
        self.option_menu = ctk.CTkOptionMenu(
            self.root,
            variable=self.boost_mode_var,
            values=[name for name, value in options],
            command=self.change_boost_mode
        )
        self.option_menu.pack(pady=10)

        # Option değer eşlemeleri
        self.options_dict = {name: value for name, value in options}
        self.values_dict = {value: name for name, value in options}

    def check_initial_state(self):
        """Get the current Processor Performance Boost Mode value."""
        current_value = get_processor_boost_mode()
        if current_value is not None:
            name = self.values_dict.get(current_value, "Unknown")
            self.boost_mode_var.set(name)
        else:
            self.boost_mode_var.set("Unknown")

    def change_boost_mode(self, selected_option):
        """Change the Processor Performance Boost Mode based on user selection."""
        value = self.options_dict[selected_option]
        if set_processor_boost_mode(value):
            messagebox.showinfo("Success", f"Processor Performance Boost Mode set to {selected_option}.")
        else:
            messagebox.showerror("Error", "Failed to change Processor Performance Boost Mode.")
            # Eski değere geri dön
            self.check_initial_state()

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = PowerModeSwitcher(root)
    root.mainloop()