import psutil
import tkinter as tk
from tkinter import ttk, messagebox

def list_processes():
    """List currently running processes with their memory usage."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            memory_usage = proc.info['memory_info'].rss / (1024 * 1024)  # Convert to MB
            processes.append((proc.info['pid'], proc.info['name'], memory_usage))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return sorted(processes, key=lambda x: x[2], reverse=True)  # Sort by memory usage

def show_processes():
    """Show processes and allow the user to terminate selected ones."""
    processes = list_processes()
    for widget in process_listbox.get_children():
        process_listbox.delete(widget)
    for pid, name, memory in processes:
        process_listbox.insert("", "end", iid=pid, values=(name, f"{memory:.2f} MB"))

def terminate_process():
    """Terminate selected process."""
    selected_item = process_listbox.selection()
    if not selected_item:
        messagebox.showinfo("No Selection", "Please select a process to terminate.")
        return

    pid = int(selected_item[0])
    try:
        proc = psutil.Process(pid)
        proc.terminate()  # or proc.suspend()
        messagebox.showinfo("Success", f"Process {proc.name()} terminated.")
        show_processes()
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        messagebox.showerror("Error", str(e))

# Create UI
root = tk.Tk()
root.title("RAM Booster")

frame = ttk.Frame(root, padding=(10, 10))
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

process_listbox = ttk.Treeview(frame, columns=("Name", "Memory"), show="headings")
process_listbox.heading("Name", text="Process Name")
process_listbox.heading("Memory", text="Memory Usage")
process_listbox.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))

list_button = ttk.Button(frame, text="List Processes", command=show_processes)
list_button.grid(row=1, column=0, sticky=(tk.W))

terminate_button = ttk.Button(frame, text="Terminate Process", command=terminate_process)
terminate_button.grid(row=1, column=1, sticky=(tk.E))

root.mainloop()