# import wmi

# open_hardware_monitor = wmi.WMI(namespace="root\\OpenHardwareMonitor")
# temperature_infos = open_hardware_monitor.Sensor()
    
# for sensor in temperature_infos:
#     if sensor.SensorType == u"Temperature":
#         print(sensor.Name)
#         print(sensor.Value)
#         print(sensor)



# import wmi

# try:
#     open_hardware_monitor = wmi.WMI(namespace="root\\OpenHardwareMonitor")
#     all_sensors = open_hardware_monitor.Sensor()
#     # Debug: Print how many sensors are returned
#     print("Number of sensors found:", len(all_sensors))

#     for sensor in all_sensors:
#         # Debug: Print sensor details even if it's not temperature
#         print("Sensor Name:", sensor.Name)
#         print("Sensor Type:", sensor.SensorType)
#         print("Sensor Value:", sensor.Value)
#         print("–––––––––––––––––––––––––––––––––––––––––––")
        
#         # Check if sensor is a temperature sensor
#         if sensor.SensorType == u"Temperature":
#             print("--- Temperature Sensor Detected ---")
#             print("Name:", sensor.Name)
#             print("Value:", sensor.Value)
#             print("Full Object:", sensor)
#             print("------------------------------------")
# except Exception as e:
#     print("An error occurred:", str(e))





import wmi

class HardwareMonitor:
    """Class to interact with OpenHardwareMonitor WMI sensors and gather hardware info."""
    def __init__(self):
        """Initialize the WMI connection to the OpenHardwareMonitor namespace."""
        try:
            self._w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            self.sensors = []
        except Exception as e:
            print("Failed to connect to WMI namespace:", str(e))
            self._w = None

    def update_info(self):
        """Retrieve all sensors from the OpenHardwareMonitor WMI namespace."""
        if not self._w:
            print("WMI connection not established.")
            return
        
        try:
            self.sensors = self._w.Sensor()
        except Exception as e:
            print("Error retrieving sensor data:", str(e))
            self.sensors = []

    def gather_info(self):
        """Process sensors and extract CPU, GPU, RAM, etc. usage and temperatures."""
        
        # Temporary dictionaries to store data
        cpu_load = None                  # e.g. CPU Total Load in %
        cpu_temp = None                  # e.g. CPU Package temperature
        cpu_cores_load = {}             # e.g. individual CPU cores load
        cpu_cores_temp = {}             # e.g. individual CPU cores temps
        gpu_load = None                 # e.g. GPU Core load
        gpu_temp = None                 # e.g. GPU Core temperature
        ram_load = None                 # e.g. Memory usage in %
        ram_used_gb = None             # e.g. Used Memory in GB
        ram_available_gb = None        # e.g. Available Memory in GB
        disk_usage_list = []           # e.g. list of used space in % for each drive
        fan_speeds = {}                # e.g. dictionary of fan name -> fan speed (RPM)
        
        # Iterate sensors and categorize them
        for sensor in self.sensors:
            s_name = sensor.Name
            s_type = sensor.SensorType
            s_value = sensor.Value
            s_id = sensor.Identifier.lower()
            
            # CPU total load
            if s_name == "CPU Total" and s_type == "Load":
                cpu_load = s_value
            
            # CPU core load
            if "CPU Core" in s_name and s_type == "Load":
                cpu_cores_load[s_name] = s_value
            
            # CPU package temperature (common reference for overall CPU temp)
            if s_name == "CPU Package" and s_type == "Temperature":
                cpu_temp = s_value
            
            # CPU core temperature
            if "CPU Core" in s_name and s_type == "Temperature":
                cpu_cores_temp[s_name] = s_value
            
            # GPU load
            if s_name == "GPU Core" and s_type == "Load":
                gpu_load = s_value
            
            # GPU temperature
            if s_name == "GPU Core" and s_type == "Temperature":
                gpu_temp = s_value
            
            # Memory usage
            if s_name == "Memory" and s_type == "Load":
                ram_load = s_value
            
            # Used Memory (GB)
            if s_name == "Used Memory" and s_type == "Data":
                ram_used_gb = s_value
            
            # Available Memory (GB)
            if s_name == "Available Memory" and s_type == "Data":
                ram_available_gb = s_value
            
            # Disk usage -> "Used Space" in multiple partitions
            if "Used Space" in s_name and s_type == "Load":
                disk_usage_list.append({s_name: s_value})
            
            # Possible fan sensor
            # (Check if sensor type is "Fan" or name includes "Fan")
            if s_type == "Fan":
                fan_speeds[s_name] = s_value
        
        # Store the final processed results in a dictionary
        hardware_info = {
            "cpu": {
                "total_load_percent": cpu_load,
                "temperature_c": cpu_temp,
                "core_loads": cpu_cores_load,
                "core_temps": cpu_cores_temp
            },
            "gpu": {
                "load_percent": gpu_load,
                "temperature_c": gpu_temp
            },
            "memory": {
                "load_percent": ram_load,
                "used_gb": ram_used_gb,
                "available_gb": ram_available_gb
            },
            "disks": disk_usage_list,
            "fans": fan_speeds
        }
        
        return hardware_info

    def get_current_info(self):
        """Convenience method to update sensors and retrieve all hardware info at once."""
        self.update_info()
        return self.gather_info()

if __name__ == "__main__":
    hm = HardwareMonitor()
    info = hm.get_current_info()

    print("=== CPU INFO ===")
    print("Total CPU Load (%):", info["cpu"]["total_load_percent"])
    print("CPU Package Temp (C):", info["cpu"]["temperature_c"])
    print("CPU Core Loads:", info["cpu"]["core_loads"])
    print("CPU Core Temps:", info["cpu"]["core_temps"])

    print("\n=== GPU INFO ===")
    print("GPU Load (%):", info["gpu"]["load_percent"])
    print("GPU Temp (C):", info["gpu"]["temperature_c"])

    print("\n=== MEMORY INFO ===")
    print("RAM Usage (%):", info["memory"]["load_percent"])
    print("Used RAM (GB):", info["memory"]["used_gb"])
    print("Available RAM (GB):", info["memory"]["available_gb"])

    print("\n=== DISK INFO ===")
    print("Disk Usages (%):", info["disks"])

    print("\n=== FAN INFO ===")
    print("Fan Speeds (RPM):", info["fans"])

