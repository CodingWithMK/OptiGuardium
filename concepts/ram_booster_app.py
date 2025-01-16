import psutil
import tkinter as tk
from tkinter import ttk, messagebox

class RAMBoosterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OptiPerformance - RAM Booster")
        self.create_widgets()

    def list_processes(self):
        """List currently running processes with their memory usage."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'create_time']):
            try:
                memory_usage = proc.info['memory_info'].rss / (1024 * 1024)  # Convert to MB
                processes.append((proc.info['pid'], proc.info['name'], memory_usage, proc.info['create_time']))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return sorted(processes, key=lambda x: x[2], reverse=True)  # Sort by memory usage

    def show_processes(self):
        """Show processes and allow the user to terminate selected ones."""
        processes = self.list_processes()
        for widget in self.process_listbox.get_children():
            self.process_listbox.delete(widget)
        for pid, name, memory, _ in processes:
            self.process_listbox.insert("", "end", iid=pid, values=(name, f"{memory:.2f} MB"))

    def terminate_process(self):
        """Terminate selected process."""
        selected_item = self.process_listbox.selection()
        if not selected_item:
            messagebox.showinfo("No Selection", "Please select a process to terminate.")
            return

        pid = int(selected_item[0])
        try:
            proc = psutil.Process(pid)
            proc.terminate()  # or proc.suspend()
            messagebox.showinfo("Success", f"Process {proc.name()} terminated.")
            self.show_processes()
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            messagebox.showerror("Error", str(e))

    def create_widgets(self):
        """Create the main UI components."""
        frame = ttk.Frame(self.root, padding=(10, 10))
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Treeview for process display
        self.process_listbox = ttk.Treeview(frame, columns=("Name", "Memory"), show="headings")
        self.process_listbox.heading("Name", text="Process Name")
        self.process_listbox.heading("Memory", text="Memory Usage")
        self.process_listbox.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E))

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.process_listbox.yview)
        self.process_listbox.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=3, sticky=(tk.N, tk.S))

        # Buttons
        list_button = ttk.Button(frame, text="List Processes", command=self.show_processes)
        list_button.grid(row=1, column=0, sticky=(tk.W))

        terminate_button = ttk.Button(frame, text="Terminate Process", command=self.terminate_process)
        terminate_button.grid(row=1, column=1, sticky=(tk.W))

if __name__ == "__main__":
    root = tk.Tk()
    app = RAMBoosterApp(root)
    root.mainloop()
