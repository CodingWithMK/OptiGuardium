import wmi

class HardwareMonitor:
    """Class to interact with OpenHardwareMonitor WMI sensors and gather hardware info."""

    def __init__(self):
        """Initialize the WMI connection to the OpenHardwareMonitor namespace."""
        print("DEBUG: Initializing WMI connection...")
        try:
            self._w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            self.sensors = []
            print("DEBUG: WMI connection established.")
        except Exception as e:
            print("Failed to connect to WMI namespace:", str(e))
            self._w = None

    def update_info(self):
        """Retrieve all sensors from the OpenHardwareMonitor WMI namespace."""
        print("DEBUG: Attempting to retrieve sensors...")
        if not self._w:
            print("DEBUG: WMI connection not established, skipping sensor retrieval.")
            return
        
        try:
            self.sensors = self._w.Sensor()
            print(f"DEBUG: {len(self.sensors)} sensors retrieved.")
        except Exception as e:
            print("Error retrieving sensor data:", str(e))
            self.sensors = []

    def gather_info(self):
        """Process sensors and extract CPU, GPU, RAM, etc. usage and temperatures."""
        if not self.sensors:
            print("DEBUG: No sensors to process, returning empty data.")
            return {}
        
        cpu_load = None
        cpu_temp = None
        gpu_load = None
        gpu_temp = None
        ram_load = None
        
        # Just do a quick debug loop:
        for sensor in self.sensors:
            print(f"DEBUG: Checking sensor - Name: {sensor.Name}, Type: {sensor.SensorType}, Value: {sensor.Value}")
            if sensor.Name == "CPU Total" and sensor.SensorType == "Load":
                cpu_load = sensor.Value
            if sensor.Name == "CPU Package" and sensor.SensorType == "Temperature":
                cpu_temp = sensor.Value
            if sensor.Name == "GPU Core" and sensor.SensorType == "Load":
                gpu_load = sensor.Value
            if sensor.Name == "GPU Core" and sensor.SensorType == "Temperature":
                gpu_temp = sensor.Value
            if sensor.Name == "Memory" and sensor.SensorType == "Load":
                ram_load = sensor.Value

        return {
            "cpu_load": cpu_load,
            "cpu_temp": cpu_temp,
            "gpu_load": gpu_load,
            "gpu_temp": gpu_temp,
            "ram_load": ram_load,
        }

    def get_current_info(self):
        """Convenience method to update sensors and retrieve all hardware info at once."""
        self.update_info()
        info = self.gather_info()
        print("DEBUG: Gathered info:", info)
        return info
    
if __name__ == "__main__":
    print("DEBUG: Starting hardware monitor test...")
    hm = HardwareMonitor()
    info = hm.get_current_info()
    print("DEBUG: Final hardware info:", info)