import psutil

def list_top_memory_consuming_processes(limit=5):
    """Lists the top memory consuming processes."""
    # Get all running processes
    processes = [proc for proc in psutil.process_iter(['pid', 'name', 'memory_info'])]

    # Sort processes by memory usage, descending
    processes.sort(key=lambda proc: proc.info['memory_info'].rss, reverse=True)

    # Print the top memory consuming processes
    print(f"\nTop {limit} memory consuming processes:")
    for proc in processes[:limit]:
        print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, RSS: {proc.info['memory_info'].rss // (1024 * 1024)} MB")

def terminate_process(pid):
    """Terminate the process with the given PID."""
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=3)
        print(f"Process {pid} terminated successfully.")
    except psutil.NoSuchProcess:
        print(f"No process with PID {pid}.")
    except psutil.AccessDenied:
        print(f"Access denied when trying to terminate PID {pid}.")
    except Exception as e:
        print(f"Error terminating process {pid}: {e}")

# Main logic
if __name__ == "__main__":
    list_top_memory_consuming_processes()

    # Ask user if they want to terminate any of the top processes
    pid_to_kill = input("Enter the PID of the process you want to terminate (or 'exit' to quit): ").strip()
    if pid_to_kill.lower() != 'exit':
        try:
            terminate_process(int(pid_to_kill))
        except ValueError:
            print("Invalid PID entered.")