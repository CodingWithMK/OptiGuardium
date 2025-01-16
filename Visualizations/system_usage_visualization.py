import tkinter as tk
import psutil
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotly.express as pltx


class SystemUsageMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("System Usage Monitor")
        self.geometry("640x480")

        self.cpu_usage_label = tk.Label(self, text="CPU Usage: 0%", font=("Arial", 12))
        self.cpu_usage_label.grid(row=0, column=0, pady=5)

        self.memory_usage_label = tk.Label(self, text="RAM Usage: 0%", font=("Arial", 12))
        self.memory_usage_label.grid(row=1, column=0, pady=5)

        # Main Menu Buttons
        self.show_visualizations_button = tk.Button(self, text='Show Hardware Visualizations', command=self.show_visualizations)
        self.show_visualizations_button.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        self.update_system_usage()

    def update_system_usage(self):
        # Get system usage information
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent

        # Update the labels with the new information
        self.cpu_usage_label.config(text=f"CPU Usage: {cpu_usage}%")
        self.memory_usage_label.config(text=f"RAM Usage: {memory_usage}%")

        # Schedule the next update after 1 second
        self.after(1000, self.update_system_usage)

    def show_visualizations(self):
        visualizations_window = VisualizationsWindow(self)

    
class VisualizationsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title('Hardware Usage Visualizations')

        # CPU Usage Label
        self.cpu_label = tk.Label(self, text='CPU Usage:')
        self.cpu_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.cpu_usage = tk.Label(self, text='')
        self.cpu_usage.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # CPU Usage Lineplot
        self.cpu_figure, self.cpu_ax = plt.subplots(figsize=(5, 3), tight_layout=True)
        self.cpu_line, = self.cpu_ax.plot([], [], label='CPU Usage')
        self.cpu_ax.set_xlabel('Time (s)')
        self.cpu_ax.set_ylabel('CPU Usage (%)')
        self.cpu_ax.legend(loc='upper left')

        # Setting y-axis percentage from 0 to 100
        self.cpu_ax.set_ylim(0, 100)

        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_figure, self)
        self.cpu_canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        # Initializing the start time
        self.start_time = time.time()

        self.update_cpu_info()


        # RAM Usage Label
        self.memory_label = tk.Label(self, text='RAM Usage:')
        self.memory_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.memory_usage = tk.Label(self, text='')
        self.memory_usage.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # RAM Usage Lineplot
        self.memory_figure, self.memory_ax = plt.subplots(figsize=(5, 3), tight_layout=True)
        self.memory_line, = self.memory_ax.plot([], [], label='RAM Usage')
        self.memory_ax.set_xlabel('Time (s)')

        # Setting y-axis percentage from 0 to 100
        self.memory_ax.set_ylim(0, 100)

        self.memory_canvas = FigureCanvasTkAgg(self.memory_figure, self)
        self.memory_canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        # Initializing the start time
        self.start_time = time.time()

        self.update_memory_info()

        # Disk Labels
        self.disk_labels = []
        self.disk_textvars = []

        for i, disk in enumerate(psutil.disk_partitions()):
            text_var = tk.StringVar()
            text_var.set(f'{disk.device}: {0.0}%')
            
            label = tk.Label(self, textvariable=text_var)
            label.grid(row=i, column=0, padx=10, pady=5, sticky='w')
            
            self.disk_labels.append(label)
            self.disk_textvars.append(text_var)

        # Disk Usage Lineplot
        self.disk_figure, self.disk_ax = plt.subplots(figsize=(5, 3), tight_layout=True)
        self.disk_lines = []
        for i in range(len(self.disk_labels)):
            line, = self.disk_ax.plot([], [], label=f'Disk {i} Usage')
            self.disk_lines.append(line)

        self.disk_ax.set_xlabel('Time (s)')
        self.disk_ax.set_ylabel('Disk Usage (%)')
        self.disk_ax.legend(loc='upper left')

        # Setting the y-axis from 0 to 100
        self.disk_ax.set_ylim(0, 100)

        self.disk_canvas = FigureCanvasTkAgg(self.disk_figure, self)
        self.disk_canvas.get_tk_widget().grid(row=len(self.disk_labels), column=0, columnspan=2, padx=10, pady=5, sticky='w')

        # Initializing the start time
        self.start_time = time.time()

        self.update_disk_info()


    def update_cpu_info(self):
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            self.cpu_usage.configure(text=f'{cpu_percent:.2f}%')

            # Updating Lineplot Data
            x_data = self.cpu_line.get_xdata()
            y_data = self.cpu_line.get_ydata()

            x_data = list(x_data) + [time.time() - self.start_time]
            y_data = list(y_data) +[cpu_percent]

            self.cpu_line.set_xdata(x_data)
            self.cpu_line.set_ydata(y_data)

            # Limiting data points to the last 10 seconds
            self.cpu_ax.set_xlim(max(0, time.time() - self.start_time - 10), time.time() - self.start_time)

            self.cpu_canvas.draw()

        except Exception as e:
            print(f'Error updating CPU info: {e}')

        self.after(1000, self.update_cpu_info)


    def update_memory_info(self):
        try:
            memory_percent = psutil.virtual_memory().percent
            self.memory_usage.configure(text=f'{memory_percent:.2f}%')

            # Updating the Lineplot
            x_data = self.memory_line.get_xdata()
            y_data = self.memory_line.get_ydata()

            x_data = list(x_data) + [time.time() - self.start_time]
            y_data = list(y_data) + [memory_percent]

            self.memory_line.set_xdata(x_data)
            self.memory_line.set_ydata(y_data)

            # Limitting data points to the last 10 seconds
            self.memory_ax.set_xlim(max(0, time.time() - self.start_time - 10), time.time() - self.start_time)

            self.memory_canvas.draw()
        
        except Exception as e:
            print(f'Error updating RAM info: {e}')

        self.after(100, self.update_memory_info)

    
    def update_disk_info(self):
        try:
            # Updating the informaion of each disk every second
            for i, (label, text_var) in enumerate(zip(self.disk_labels, self.disk_textvars)):
                device_path = text_var.get().split(':')[0]
                if not device_path.endswith(':\\'):
                    device_path += ':\\'

                disk_usage = psutil.disk_usage(device_path)

                text_var.set(f'{device_path}: {disk_usage.percent:.2f}%')

                # Updating Lineplot
                x_data = self.disk_lines[i].get_xdata()
                y_data = self.disk_lines[i].get_ydata()

                x_data = list(x_data) + [time.time() - self.start_time]
                y_data = list(y_data) + [disk_usage.percent]

                self.disk_lines[i].set_xdata(x_data)
                self.disk_lines[i].set_ydata(y_data)

                # Limitting data points to the last 10 seconds
                self.disk_ax.set_xlim(max(0, time.time() - self.start_time - 10), time.time() - self.start_time)
                    
            self.disk_canvas.draw()

        except Exception as e:
            print(f'Error updating disk info: {e}')

        self.after(1000, self.update_disk_info)

if __name__ == "__main__":
    app = SystemUsageMonitor()
    app.mainloop()