import os
import sys
import subprocess
import re
from bs4 import BeautifulSoup

class BatteryStats():
    def __init__(self):
        
        # self.battery_report_path = os.path.expanduser("~\\battery-report.html")
        # Get access to the battery report on the current drive
        self.battery_report_path = os.path.join(os.getcwd(), "battery-report.html")
        self.generate_battery_report()
        self.html_content = self.read_battery_report()
        self.parse_html_content()

    def generate_battery_report(self):
        # Generate the battery report using the 'powercfg' command
        try:
            subprocess.run(["powercfg", "/batteryreport"], check=True)
        except subprocess.CalledProcessError as error:
            print(f"Error generating battery report: {error}")

    def read_battery_report(self):
        # Read the HTML content from the battery report file
        try:
            with open(self.battery_report_path, 'r') as battery_report_file:
                html_content = battery_report_file.read()
                return html_content
        except FileNotFoundError as error:
            print(f"{error}\nBattery report file not found at: {self.battery_report_path}")
        return ""
    
    def parse_html_content(self):
        # Parse HTML content
        if not self.html_content:
            return
        
        soup = BeautifulSoup(self.html_content, 'html.parser')
        
        # Getting access to the values "Charge Capacity" and "Full Charge Capacity"
        # Charge capacity values are stored under table tags

        model_name = self.find_value(soup, "SYSTEM PRODUCT NAME")
        manufacturer = self.find_value(soup, "MANUFACTURER")
        serial_number = self.find_value(soup, "SERIAL NUMBER")
        chemistry = self.find_value(soup, "CHEMISTRY")
        design_capacity = self.find_value(soup, "DESIGN CAPACITY")
        full_charge_capacity = self.find_value(soup, "FULL CHARGE CAPACITY")

        # Converting "design_capacity" and "full_charge_capacity" values into only digits
        _design_capacity = re.sub(r'[^0-9]', '', design_capacity)
        _full_charge_capacity = re.sub(r'[^0-9]', '', full_charge_capacity)

        # Calculating "current_cahrge_capacity" in percent
        current_charge_capcity = f"{float(_full_charge_capacity) / float(_design_capacity) * 100:.2f}%"

        battery_stats = {
            "Model Name": model_name,
            "Manufacturer": manufacturer,
            "Serial Number": serial_number,
            "Chemistry": chemistry,
            "Design Capacity": _design_capacity,
            "Full Charge Capacity": _full_charge_capacity,
            "Current Charge Capacity": current_charge_capcity
        }

        return battery_stats

        # Print battery stats
        # print(f"Model Name: {model_name}")
        # print(f"Manufacturer: {manufacturer}")
        # print(f"Serial Number: {serial_number}")
        # print(f"Chemistry: {chemistry}")
        # print(f"Design Capacity: {_design_capacity} mAh => 100%")
        # print(f"Full Charge Capacity: {_full_charge_capacity} mAh => {current_charge_capcity:.2f}%")

    def find_value(self, soup, label):
        # Locating spans that is containing the desired data
        element = soup.find('span', class_="label", string=label)
        if element:
            parent_td = element.find_parent('td')
            next_td = parent_td.find_next_sibling('td') if parent_td else None
            if next_td:
                return next_td.text.strip()
        
        return "N/A"
    
    # def run_battery_report(self):
    #     self.generate_battery_report()
    #     self.read_battery_report()
    #     self.parse_html_content()
    

if __name__ == "__main__":
    BatteryStats()

