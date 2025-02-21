import wmi

class LibreHardwareMonitor:
    """Class to interact with LibreHardwareMonitor WMI sensors and gather hardware info."""

    def __init__(self):
        """Initialize the WMI connection to the LibreHardwareMonitor namespace."""
        try:
            # Connect to "root\\LibreHardwareMonitor" 
            self._w = wmi.WMI(namespace="root\\LibreHardwareMonitor")
            self.sensors = []
        except Exception as e:
            print("Failed to connect to WMI namespace (LibreHardwareMonitor):", str(e))
            self._w = None

    def update_info(self):
        """Retrieve all sensors from the LibreHardwareMonitor WMI namespace."""
        if not self._w:
            print("WMI connection not established. Make sure LibreHardwareMonitor is running.")
            self.sensors = []
            return
        
        try:
            self.sensors = self._w.Sensor()
        except Exception as e:
            print("Error retrieving sensor data:", str(e))
            self.sensors = []

    def gather_info(self):
        """
        Process sensors and extract CPU, GPU, iGPU, RAM, disk, network, and battery info.
        NOTE: You must adapt sensor names/types to match what your system actually reports.
        """
        
        # Basic CPU info
        cpu_load = None
        cpu_temp = None
        
        # Discrete GPU info
        gpu_load = None
        gpu_temp = None
        gpu_memory_usage = None  # e.g., VRAM usage in %
        
        # Integrated GPU info
        igpu_usage = None
        igpu_memory_usage = None
        
        # RAM info
        ram_load = None
        used_ram_gb = None
        available_ram_gb = None
        
        # Disk info: we'll store a list of dicts with temperature, activity, etc.
        disks = []
        
        # Network info: store as dictionary keyed by adapter (ethernet, wifi, etc.)
        # We'll guess sensor names like "Ethernet Download", "Ethernet Upload", "Wi-Fi Download", "Wi-Fi Upload".
        network_info = {
            "ethernet": {
                "download_mbps": None,
                "upload_mbps": None,
                "usage_percent": None  # if there's a usage load sensor
            },
            "wifi": {
                "download_mbps": None,
                "upload_mbps": None,
                "usage_percent": None
            }
        }
        
        # Battery info
        battery_info = {
            "voltage_v": None,
            "current_a": None,
            "power_w": None,
            "capacity_percent": None
        }
        
        # We'll gather raw disk temperature by looking for sensor type "Temperature" 
        # and disk usage by "Load" with names like "Used Space" or "Total Activity".
        # We'll store them in a dictionary based on sensor.Name or sensor.Identifier.
        
        # Iterate over all sensors
        for sensor in self.sensors:
            name = sensor.Name
            s_type = sensor.SensorType
            value = sensor.Value
            identifier = getattr(sensor, "Identifier", "")
            
            # CPU
            if name == "CPU Total" and s_type == "Load":
                cpu_load = value
            if name == "CPU Package" and s_type == "Temperature":
                cpu_temp = value
            
            # Discrete GPU
            if name == "GPU Core" and s_type == "Load":
                gpu_load = value
            if name == "GPU Core" and s_type == "Temperature":
                gpu_temp = value
            if name == "GPU Memory" and s_type == "Load":
                gpu_memory_usage = value  # VRAM usage in %
            
            # Integrated GPU (example names: "D3D 3D" for usage, "D3D Memory" for memory usage)
            # You need to adapt to your real sensor names
            if name == "D3D 3D" and s_type == "Load":
                igpu_usage = value
            if name == "D3D Memory" and s_type == "Load":
                igpu_memory_usage = value
            
            # RAM
            if name == "Memory" and s_type == "Load":
                ram_load = value
            if name == "Used Memory" and s_type == "Data":
                used_ram_gb = value
            if name == "Available Memory" and s_type == "Data":
                available_ram_gb = value
            
            # Disks (temperature / usage)
            # We'll guess that if sensor type == "Temperature" and "ssd"/"hdd"/"nvme" is in identifier, it's a disk temp
            # or if name contains "Temperature" and parent is a storage device.
            # We'll also guess "Used Space" or "Total Activity" for usage.
            if s_type == "Temperature" and any(x in identifier.lower() for x in ["hdd", "ssd", "nvme"]):
                # We'll store it as {"identifier": identifier, "temp": value}
                disks.append({
                    "identifier": identifier,
                    "name": name,
                    "temperature_c": value
                })
            
            # By default, LibreHardwareMonitor might show "Used Space" (Load) for each disk partition
            if "Used Space" in name and s_type == "Load":
                disks.append({
                    "identifier": identifier,
                    "name": name,
                    "used_space_percent": value
                })
            
            # Bazı sistemler "Total Activity" (Load) diye bir sensör verir.
            if "Total Activity" in name and s_type == "Load":
                disks.append({
                    "identifier": identifier,
                    "name": name,
                    "activity_percent": value
                })
            
            # Network
            # Örnek: "Ethernet Download", "Ethernet Upload", "Wi-Fi Download", "Wi-Fi Upload" vb.  
            if "Ethernet" in name and "Download" in name and s_type == "Throughput":
                # value might be in MB/s or Bytes/s, you can convert to Mbps
                network_info["ethernet"]["download_mbps"] = value * 8  # if value is MB/s -> MB x 8 = Mbps
            if "Ethernet" in name and "Upload" in name and s_type == "Throughput":
                network_info["ethernet"]["upload_mbps"] = value * 8
            if "Ethernet" in name and s_type == "Load":
                network_info["ethernet"]["usage_percent"] = value
            
            if "Wi-Fi" in name and "Download" in name and s_type == "Throughput":
                network_info["wifi"]["download_mbps"] = value * 8
            if "Wi-Fi" in name and "Upload" in name and s_type == "Throughput":
                network_info["wifi"]["upload_mbps"] = value * 8
            if "Wi-Fi" in name and s_type == "Load":
                network_info["wifi"]["usage_percent"] = value
            
            # Battery
            # LibreHardwareMonitor bazen "Battery" altında "Voltage", "Current", "Power", "Level" vb. isimler kullanabiliyor.
            if "Battery" in identifier.lower() or "battery" in name.lower():
                # We guess some sensor types
                if s_type == "Voltage":
                    battery_info["voltage_v"] = value
                if s_type == "Current":
                    battery_info["current_a"] = value
                if s_type == "Power":
                    battery_info["power_w"] = value
                # Might be "Level" or "Charge" or "Capacity" 
                if "Level" in name or "Capacity" in name:
                    battery_info["capacity_percent"] = value
        
        # Build the dictionary with gathered info
        hardware_info = {
            "cpu": {
                "total_load_percent": cpu_load,
                "temperature_c": cpu_temp
            },
            "gpu": {
                "core_load_percent": gpu_load,
                "temperature_c": gpu_temp,
                "memory_load_percent": gpu_memory_usage
            },
            "igpu": {
                "load_percent": igpu_usage,
                "memory_load_percent": igpu_memory_usage
            },
            "memory": {
                "load_percent": ram_load,
                "used_gb": used_ram_gb,
                "available_gb": available_ram_gb
            },
            "disks": disks,
            "network": network_info,
            "battery": battery_info
        }
        
        return hardware_info

    def get_current_info(self):
        """Convenience method to update sensors and retrieve all hardware info at once."""
        self.update_info()
        return self.gather_info()
    

if __name__ == "__main__":
    lhm = LibreHardwareMonitor()
    info = lhm.get_current_info()

    # Print out the results. Adjust as needed.
    print("=== CPU INFO ===")
    print("CPU Total Load (%):", info["cpu"]["total_load_percent"])
    print("CPU Package Temp (C):", info["cpu"]["temperature_c"])

    print("\n=== DISCRETE GPU INFO ===")
    print("GPU Core Load (%):", info["gpu"]["core_load_percent"])
    print("GPU Temp (C):", info["gpu"]["temperature_c"])
    print("GPU Memory Usage (%):", info["gpu"]["memory_load_percent"])

    print("\n=== INTEGRATED GPU INFO ===")
    print("iGPU Load (%):", info["igpu"]["load_percent"])
    print("iGPU Memory Usage (%):", info["igpu"]["memory_load_percent"])

    print("\n=== MEMORY INFO ===")
    print("RAM Usage (%):", info["memory"]["load_percent"])
    print("Used RAM (GB):", info["memory"]["used_gb"])
    print("Available RAM (GB):", info["memory"]["available_gb"])

    print("\n=== DISK INFO ===")
    for disk_data in info["disks"]:
        print(disk_data)

    print("\n=== NETWORK INFO ===")
    print("Ethernet:", info["network"]["ethernet"])
    print("Wi-Fi:", info["network"]["wifi"])

    print("\n=== BATTERY INFO ===")
    print(info["battery"])


