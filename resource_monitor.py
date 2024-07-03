import psutil
import smtplib
from email.mime.text import MIMEText
from slack_sdk import WebClient
from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

# Chargez vos variables d'environnement depuis le fichier .env
load_dotenv(dotenv_path='.env/data.env')

# Définissez les seuils à partir desquels vous voulez créer vos alertes
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 35
DISK_THRESHOLD = 35

def send_email_alert(subject, message):
    # Configurez les paramètres SMTP à partir des variables d'environnement
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')

    # Créez votre message avec vos parametres
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = 'your.email@gmail.com'  

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

def send_slack_alert(message):
    slack_token = os.getenv('SLACK_TOKEN')
    client = WebClient(token=slack_token)

    response = client.chat_postMessage(channel='#alerts', text=message)

def monitor_resources():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        update_gui(cpu_usage, memory_usage, disk_usage)

        if cpu_usage > CPU_THRESHOLD:
            send_email_alert('CPU Alert', f'CPU usage is {cpu_usage}%')
            send_slack_alert(f'CPU usage is {cpu_usage}%')
        if memory_usage > MEMORY_THRESHOLD:
            send_email_alert('Memory Alert', f'Memory usage is {memory_usage}%')
            send_slack_alert(f'Memory usage is {memory_usage}%')
        if disk_usage > DISK_THRESHOLD:
            send_email_alert('Disk Alert', f'Disk usage is {disk_usage}%')
            send_slack_alert(f'Disk usage is {disk_usage}%')

        time.sleep(1)

def update_gui(cpu, memory, disk):
    cpu_var.set(f'CPU Usage: {cpu}%')
    memory_var.set(f'Memory Usage: {memory}%')
    disk_var.set(f'Disk Usage: {disk}%')

    cpu_values.append(cpu)
    memory_values.append(memory)
    disk_values.append(disk)

    if len(cpu_values) > 100:
        cpu_values.pop(0)
        memory_values.pop(0)
        disk_values.pop(0)

    ax_cpu.clear()
    ax_memory.clear()
    ax_disk.clear()

    ax_cpu.plot(cpu_values, label='CPU Usage')
    ax_memory.plot(memory_values, label='Memory Usage')
    ax_disk.plot(disk_values, label='Disk Usage')

    ax_cpu.legend(loc='upper right')
    ax_memory.legend(loc='upper right')
    ax_disk.legend(loc='upper right')

    canvas.draw()

root = tk.Tk()
root.title('System Resource Monitor')

cpu_var = tk.StringVar()
memory_var = tk.StringVar()
disk_var = tk.StringVar()

ttk.Label(root, textvariable=cpu_var).pack()
ttk.Label(root, textvariable=memory_var).pack()
ttk.Label(root, textvariable=disk_var).pack()

fig, (ax_cpu, ax_memory, ax_disk) = plt.subplots(3, 1, figsize=(6, 6))
cpu_values = []
memory_values = []
disk_values = []

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

threading.Thread(target=monitor_resources, daemon=True).start()

root.mainloop()