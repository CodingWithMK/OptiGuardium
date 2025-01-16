import customtkinter
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from threading import Thread
from functools import cache

class HardwareMonitorApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Hardware Monitor")

        # Hardware Monitor Widgets
        self.cpu_label = customtkinter.CTkLabel(self, text='CPU:')
        self.cpu_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.ram_label = customtkinter.CTkLabel(self, text='RAM:')
        self.ram_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        # Figure for matplotlib
        self.figure, self.ax = plt.subplots()
        self.cpu_line, = self.ax.plot([], [], 'r-', label='CPU')
        self.ram_line, = self.ax.plot([], [], 'b-', label='RAM')
        self.ax.set_xlim(0, 60)
        self.ax.set_ylim(0, 100)
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Usage (%)')
        self.ax.legend()

        # Canvas for matplotlib
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=2, padx=10, pady=5, sticky='nsew')

        # Data and time lists
        self.times = []
        self.cpu_usage = []
        self.ram_usage = []

        # Starting the thread for updating usage graph
        self.update_thread = Thread(target=self.update_graph, daemon=True)
        self.update_thread.start()
        
        
        # Start updating the hardware monitor
        self.update_hardware_info()

    @cache
    def update_hardware_info(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        ram_percent = psutil.virtual_memory().percent

        # Updating CPU Percentage Display
        self.cpu_label.configure(text=f"CPU: {cpu_percent:.2f}%")
        # Updating RAM Percentage Display
        self.ram_label.configure(text=f"RAM: {ram_percent:.2f}%")

        self.after(1000, self.update_hardware_info)

    def update_graph(self):
        start_time = time.time()

        while True:
            current_time = time.time() - start_time
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent

            # Updating data and time lists
            self.times.append(current_time)
            self.cpu_usage.append(cpu_usage)
            self.ram_usage.append(ram_usage)

            # Limitting the lists to store only data of first 60 seconds
            # if len(self.times) > 60:
            #     self.times.pop(0)
            #     self.cpu_usage.pop(0)
            #     self.ram_usage.pop(0)


            # Updating graph
            self.cpu_line.set_xdata(self.times)
            self.cpu_line.set_ydata(self.cpu_usage)
            self.ram_line.set_xdata(self.times)
            self.ram_line.set_ydata(self.ram_usage)
            self.ax.set_xlim(max(0, current_time - 60), current_time)

            # Redrawing the graph
            self.canvas.draw()

if __name__ == "__main__":
    app = HardwareMonitorApp()
    app.mainloop()

