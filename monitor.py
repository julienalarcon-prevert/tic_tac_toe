import psutil
import platform
import socket
import os
from datetime import datetime, timedelta
from flask import Flask, render_template

app = Flask(__name__)

# Function to find the machine's IP address (using psutil to check if it's an IPv4 address)
def get_ip_address():
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                if interface != 'lo':  # Check that it's not the loopback interface (internal interface)
                    return addr.address
    return 'IP address not found'

# Function to gather information about all processes
def get_processes_info():
    processes_info = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        # Create a dictionary to store process information
        processes_info.append({
            'pid': proc.info['pid'],
            'name': proc.info['name'],
            'cpu_percent': proc.info['cpu_percent'],
            'memory_percent': proc.info['memory_percent']
        })
    return processes_info

# Function to collect all processes, sort them by CPU usage, and return the top 3 heaviest ones
def get_top_processes():
    processes = [(p.info['cpu_percent'], p.info['name'], p.info['pid']) for p in psutil.process_iter(['cpu_percent', 'name', 'pid'])]
    processes.sort(reverse=True, key=lambda x: x[0])  # Sort processes by CPU usage in descending order
    return [{"name": p[1], "cpu_percent": p[0], "pid": p[2]} for p in processes[:3]]  # Return top 3 processes

# Function to analyze the files in a given directory and count file types
def analyze_files_in_directory(directory):
    file_count = {
        '.txt': 0,
        '.py': 0,
        '.pdf': 0,
        '.jpg': 0,
    }

    total_files = 0

    # Walk through the directory to count files and their extensions
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            total_files += 1
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension in file_count:
                file_count[file_extension] += 1

    file_percentages = {}
    # Calculate the percentage of each file type
    if total_files > 0:
        for ext, count in file_count.items():
            file_percentages[ext] = (count / total_files) * 100
    else:
        file_percentages = {ext: 0 for ext in file_count}  # Avoid division by zero if no files are found

    return file_count, file_percentages, total_files

@app.route('/')
def index():
    boot_time = psutil.boot_time()  # Get the system boot time
    boot_time_str = datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')

    now = datetime.now()
    uptime_seconds = int(now.timestamp()) - int(boot_time)  
    uptime = str(timedelta(seconds=uptime_seconds))  # Convert uptime to a readable format

    # Gather system information to display in the template
    system_info = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "machine_name": platform.node(),  
        "oprating_system": platform.platform(),  
        "uptime": uptime, 
        "numbers_user": psutil.users(),  
        "core": psutil.cpu_count(logical=False),  
        "frequency": psutil.cpu_freq().current,  
        "usage_rate": psutil.cpu_percent(interval=1),  # CPU usage percentage (measured over 1 second)
        "RAM": round(psutil.virtual_memory().total / 1000000000, 2),  
        "RAM_used": round(psutil.virtual_memory().used / 1000000000, 2),  
        "progress": psutil.virtual_memory().percent,  
        "IP_Address": get_ip_address(),  
        "processes_info": get_processes_info(),  
        "Top_3": get_top_processes(),  
    }

    # Analyze files in a specific directory
    directory = '/home/kiki/Documents'
    file_count, file_percentages, total_files = analyze_files_in_directory(directory)

    # Update system information with file analysis data
    system_info.update({
        'file_count': file_count,
        'file_percentages': file_percentages,
        'total_files': total_files
    })

    return render_template('index.html', **system_info)  # Pass all system information to the template

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
