import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
import psutil
import platform
import subprocess
import time
import re  # For extracting numeric temperature values


class MacSystemInfoMonitor(ttk.Window):
    def __init__(self):
        super().__init__()

        self.title("Mac System Information")
        self.geometry("800x600")

        # Configure the main window with a sidebar and a main content area
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.rowconfigure(0, weight=1)

        # Configure sidebar frame
        self.sidebar = ttk.Frame(self)
        self.sidebar.grid(row=0, column=0, sticky="nswe", padx=5, pady=5)
        self.sidebar.columnconfigure(0, weight=1)

        # Configure main content frame
        self.content = ttk.Frame(self)
        self.content.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)

        # Create sidebar tab buttons
        tab_names = ["System", "CPU", "Memory", "Disk", "Network"]
        for index, name in enumerate(tab_names):
            button = ttk.Button(self.sidebar, text=name, command=lambda n=name: self.show_tab(n))
            button.grid(row=index, column=0, padx=5, pady=5, sticky="ew")

        # Create a tab for each hardware category
        self.tabs = {}
        self.tabs["System"] = self.system_tab(self.content)
        self.tabs["CPU"] = self.cpu_tab(self.content)
        self.tabs["Memory"] = self.memory_tab(self.content)
        self.tabs["Disk"] = self.disk_tab(self.content)
        self.tabs["Network"] = self.network_tab(self.content)

        # Initially display the "System" tab
        self.show_tab("System")

        # Start dynamic widget updates (every 1 second)
        self.update_dynamic_widgets()

    # ---------------- Tab Creation Methods ----------------

    def system_tab(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=0, sticky="nsew")
        # Display static system information using Labels
        title_label = ttk.Label(frame, text="System Information:", anchor="w")
        title_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        sys_info = "\n".join(self.get_system_info())
        info_label = ttk.Label(frame, text=sys_info, anchor="w", justify="left")
        info_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        return frame

    def cpu_tab(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=0, sticky="nsew")

        # Create a top frame for CPU usage and core meters
        top_frame = ttk.Frame(frame)
        top_frame.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Left side: CPU Usage Meter
        cpu_usage_label = ttk.Label(top_frame, text="CPU Usage:", anchor="w")
        cpu_usage_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.cpu_usage_meter = ttk.Meter(
            top_frame,
            bootstyle="success",
            metersize=120,
            amountused=psutil.cpu_percent(),
            padding=10,
            metertype="full",
            interactive=False
        )
        self.cpu_usage_meter.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # Right side: CPU Core Meters (arranged vertically)
        self.cpu_core_frame = ttk.Frame(top_frame)
        self.cpu_core_frame.grid(row=0, column=2, rowspan=2, sticky="ns", padx=5, pady=5)
        num_cores = psutil.cpu_count(logical=True)
        self.cpu_core_meters = []
        for i in range(num_cores):
            core_meter = ttk.Meter(
                self.cpu_core_frame,
                bootstyle="info",
                metersize=120,
                amountused=0,
                padding=5,
                metertype="full",
                interactive=False,
                subtext=f"Core {i}"
            )
            core_meter.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            self.cpu_core_meters.append(core_meter)

        # Create a bottom frame for CPU frequency and temperature meters
        bottom_frame = ttk.Frame(frame)
        bottom_frame.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        # CPU Frequency Meter
        cpu_freq_label = ttk.Label(bottom_frame, text="CPU Frequency (MHz):", anchor="w")
        cpu_freq_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.cpu_frequency_meter = ttk.Meter(
            bottom_frame,
            bootstyle="success",
            metersize=120,
            amountused=0,
            padding=10,
            metertype="full",
            interactive=False
        )
        self.cpu_frequency_meter.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # CPU Temperature Meter
        cpu_temp_label = ttk.Label(bottom_frame, text="CPU Temperature (°C):", anchor="w")
        cpu_temp_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.cpu_temperature_meter = ttk.Meter(
            bottom_frame,
            bootstyle="danger",
            metersize=120,
            amountused=0,
            padding=10,
            metertype="full",
            interactive=False
        )
        self.cpu_temperature_meter.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        return frame

    def memory_tab(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=0, sticky="nsew")
        # Row 0: Memory Usage Meter
        memory_usage_label = ttk.Label(frame, text="Memory Usage:", anchor="w")
        memory_usage_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.memory_meter = ttk.Meter(
            frame,
            bootstyle="success",
            metersize=120,
            amountused=psutil.virtual_memory().percent,
            padding=10,
            metertype="full",
            interactive=False
        )
        self.memory_meter.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        # Row 1: Memory Information Label
        memory_info_label = ttk.Label(frame, text="Memory Info:", anchor="w")
        memory_info_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.memory_info_text = ttk.Label(frame, text="", anchor="w", justify="left")
        self.memory_info_text.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        return frame

    def disk_tab(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=0, sticky="nsew")
        # Row 0: Disk Usage Meter
        disk_usage_label = ttk.Label(frame, text="Disk Usage:", anchor="w")
        disk_usage_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        disk_usage_percent = psutil.disk_usage("/").percent
        self.disk_meter = ttk.Meter(
            frame,
            bootstyle="success",
            metersize=120,
            amountused=disk_usage_percent,
            padding=10,
            metertype="full",
            interactive=False
        )
        self.disk_meter.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        # Row 1: Disk Information Label
        disk_info_label = ttk.Label(frame, text="Disk Info:", anchor="w")
        disk_info_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.disk_info_text = ttk.Label(frame, text="", anchor="w", justify="left")
        self.disk_info_text.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        return frame

    def network_tab(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=0, sticky="nsew")
        # Row 0: Network Information Label
        network_info_label = ttk.Label(frame, text="Network Info:", anchor="w")
        network_info_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.network_info_text = ttk.Label(frame, text="", anchor="w", justify="left")
        self.network_info_text.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        return frame

    def show_tab(self, tab_name):
        # Hide all tab frames and show the selected one
        for frame in self.tabs.values():
            frame.grid_remove()
        self.tabs[tab_name].grid(row=0, column=0, sticky="nsew")

    # ---------------- Dynamic Update Method ----------------

    def update_dynamic_widgets(self):
        # Update CPU tab widgets
        # CPU Usage
        cpu_usage = psutil.cpu_percent(interval=None)
        self.cpu_usage_meter.configure(amountused=cpu_usage)

        # CPU Frequency
        cpu_freq = psutil.cpu_freq()
        current_freq = cpu_freq.current if cpu_freq else 0.0
        self.cpu_frequency_meter.configure(amountused=current_freq)

        # CPU Temperature
        cpu_temp = self.get_cpu_temperature()
        self.cpu_temperature_meter.configure(amountused=cpu_temp)

        # Update each CPU Core Meter with usage percentage
        core_percentages = psutil.cpu_percent(interval=None, percpu=True)
        for i, percentage in enumerate(core_percentages):
            if i < len(self.cpu_core_meters):
                self.cpu_core_meters[i].configure(amountused=percentage)

        # Update Memory tab widgets
        mem = psutil.virtual_memory()
        self.memory_meter.configure(amountused=mem.percent)
        mem_info = (
            f"Total: {self.size_converter(mem.total)}\n"
            f"Available: {self.size_converter(mem.available)}\n"
            f"Used: {self.size_converter(mem.used)}"
        )
        self.memory_info_text.config(text=mem_info)

        # Update Disk tab widgets
        disk = psutil.disk_usage("/")
        self.disk_meter.configure(amountused=disk.percent)
        disk_info = (
            f"Total: {self.size_converter(disk.total)}\n"
            f"Used: {self.size_converter(disk.used)}\n"
            f"Free: {self.size_converter(disk.free)}\n"
            f"Usage: {disk.percent}%"
        )
        self.disk_info_text.config(text=disk_info)

        # Update Network tab widgets
        net = psutil.net_io_counters()
        network_info = (
            f"Bytes Sent: {self.size_converter(net.bytes_sent)}\n"
            f"Bytes Received: {self.size_converter(net.bytes_recv)}"
        )
        self.network_info_text.config(text=network_info)

        # Schedule the next update after 1 second
        self.after(1000, self.update_dynamic_widgets)

    # ---------------- Helper Methods ----------------

    def size_converter(self, size):
        # Converts a size in bytes to a human-readable format
        i = 0
        num = 2**10
        units = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > num:
            size /= num
            i += 1
        return f"{size:.2f}{units[i]}B"

    def get_system_info(self) -> list:
        # Returns basic system information as a list of strings
        system_info = platform.uname()
        system_os = f"System OS: {system_info.system}"
        system_release = f"System Release: {system_info.release}"
        system_architecture = f"Machine Architecture: {system_info.machine}"
        system_processor = f"Processor: {system_info.processor}"
        return [system_os, system_release, system_architecture, system_processor]

    def get_cpu_temperature(self) -> float:
        """
        Returns the CPU temperature in Celsius.
        For macOS, it runs the 'osx-cpu-temp' command.
        For Windows, it attempts to use psutil.sensors_temperatures().
        """
        system = platform.system()
        if system == "Darwin":
            try:
                # Run the 'osx-cpu-temp' command on macOS
                result = subprocess.run(['osx-cpu-temp'], capture_output=True, text=True)
                if result.returncode == 0:
                    # Expecting output like "66.2°C", extract the numeric part
                    output = result.stdout.strip()
                    match = re.search(r"([\d\.]+)", output)
                    if match:
                        return float(match.group(1))
                    else:
                        return 0.0
                else:
                    print("osx-cpu-temp command failed.")
                    return 0.0
            except Exception as e:
                print("Failed to get CPU temperature:", e)
                return 0.0
        elif system == "Windows":
            try:
                temps = psutil.sensors_temperatures()
                if "coretemp" in temps:
                    core_temps = [temp.current for temp in temps["coretemp"]]
                    if core_temps:
                        return sum(core_temps) / len(core_temps)
                return 0.0
            except Exception as e:
                print("Failed to get CPU temperature:", e)
                return 0.0
        else:
            return 0.0


if __name__ == "__main__":
    app = MacSystemInfoMonitor()
    app.mainloop()
