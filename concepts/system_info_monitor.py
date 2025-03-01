import psutil
import tkinter as tk
import ttkbootstrap
import os
import sys
import clr
import wmi

class SystemInformationMonitor(ttkbootstrap.Window):
    def __init__(self):
        super().__init__()

        self.openhardwaremonitor_hwtypes = ["Mainboard", "SuperIO", "CPU", "RAM", "GpuNvidia", "GpuAti", "TBalancer", "Heatmaster", "HDD"]
        self.cputhermometer_hwtypes = ["Mainboard", "SuperIO", "CPU", "GpuNvidia", "GpuAti", "TBalancer", "Heatmaster", "HDD"]
        self.openhardwaremonitor_sensortypes = ["Voltage", "Clock", "Temperature", "Load", "Fan", "Flow", "Control", "Level", "Factor", "Power", "Data", "SmallData"]
        self.openhardwaremonitor_sensortypes = ["Voltage", "Clock", "Temperature", "Load", "Fan", "Flow", "Control", "Level"]
        
        self.title("System Information Monitor")
        self.geometry("800x600")

        self.cpu_usage_label = ttkbootstrap.Label(self, text="CPU Usage: 0%", font=("Arial", 12))
        self.cpu_usage_label.grid(row=0, column=0, padx=10, pady=10)

        self.cpu_meter = ttkbootstrap.Meter(self, metersize=120, amountused=0, padding=10, metertype="full", interactive=False)
        self.cpu_meter.grid(row=1, column=1, padx=10, pady=10)

        self.cpu_temperature_label = ttkbootstrap.Label(self, text="CPU Temperature: 0°C", font=("Arial", 12))
        self.cpu_temperature_label.grid(row=0, column=1, padx=10, pady=10)

        self.memory_usage_label = ttkbootstrap.Label(self, text="RAM Usage: 0%", font=("Arial", 12))
        self.memory_usage_label.grid(row=1, column=0, padx=10, pady=10)

        self.memory_meter = ttkbootstrap.Meter(self, metersize=120, amountused=0, padding=10, metertype="full", interactive=False)
        self.memory_meter.grid(row=2, column=1, padx=10, pady=10)

        self.disk_usage_label = ttkbootstrap.Label(self, text="Disk Usage: 0%", font=("Arial", 12))
        self.disk_usage_label.grid(row=2, column=0, padx=10, pady=10)

        self.update_system_usage()

    def init_cpu_temp(self):
        open_hardware_monitor = wmi.WMI(namespace="root\OpenHardwareMonitor")
        temperature_infos = open_hardware_monitor.Sensor()

        for sensor in temperature_infos:
            if sensor.SensorType == u"Temperature":
                print(sensor.Name)
                print(sensor.Value)

    def update_system_usage(self):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent

        self.cpu_usage_label.config(text=f"CPU Usage: {cpu_usage:.2f}%")
        self.memory_usage_label.config(text=f"RAM Usage: {memory_usage:.2f}%")

        self.after(1000, self.update_system_usage)

if __name__ == "__main__":
    window = SystemInformationMonitor()
    window.mainloop()

        

