import psutil
import schedule
import time
import logging

# Function to logging messages
def log_message(message):
    # Configuring logging
    logging.basicConfig(filename='system_monitoring.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info(message)

# Function to print alerts to the console
def print_alert(message):
    print(f"ALERT: {message}")

# Health check functions
def check_cpu_usage(threshold=50):
    cpu_usage = psutil.cpu_percent(interval=1)

    if cpu_usage > threshold:
        mesage = f"High CPU usage detected: {cpu_usage}%"
        log_message(mesage)
        print_alert(mesage)

def check_memory_usage(threshold=80):
    memory_usage = psutil.virtual_memory().percent

    if memory_usage > threshold:
        mesage = f"High memory usage detected: {memory_usage}%"
        log_message(mesage)
        print_alert(mesage)

def check_disk_space(path='/', threshold=75):
    disk_usage = psutil.disk_usage(path).percent

    if disk_usage > threshold:
        mesage = f"Low disk space detected: {disk_usage}%"
        log_message(mesage)
        print_alert(mesage)

def check_network_traffic(threshold=100*1024 *1024):
    network_traffic = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent

    if network_traffic > threshold:
        mesage = f"High network traffic detected: {network_traffic:.2f} MB"
        
        log_message(mesage)
        print_alert(mesage)

# Main function
def run_health_checks():
    print("Monitoring the system...")
    log_message("Running system health checks...")

    check_cpu_usage()
    check_memory_usage()
    check_disk_space()
    check_network_traffic()

    log_message("System health check completed.")

# Scheduling health checks to run every half an hour
schedule.every(30).minutes.do(run_health_checks)

# Main loop to run scheduled task
while True:
    schedule.run_pending()
    time.sleep(1)