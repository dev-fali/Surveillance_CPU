import psutil

def check_resources(threshold=80):
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    if cpu_usage > threshold:
        print(f'CPU usage is {cpu_usage}%')
    if memory_usage > threshold:
        print(f'Memory usage is {memory_usage}%')
    if disk_usage > threshold:
        print(f'Disk usage is {disk_usage}%')

check_resources()
