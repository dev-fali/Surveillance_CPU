import psutil
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import getpass

#lang = input("Choose your langage english (en) or french (fr) ?") 
CPU_THRESHOLD = int(input("Veuillez entrer le seuil d'alerte pour le CPU (en %): "))
MEMORY_THRESHOLD = int(input("Veuillez entrer le seuil d'alerte pour la mémoire (en %): "))
DISK_THRESHOLD = int(input("Veuillez entrer le seuil d'alerte pour le disque (en %): "))
send_email_alerts = input("Souhaitez-vous activer les alertes par email ? (Oui/Non): ").lower() == 'oui'

if send_email_alerts:
    alert_email = input("Veuillez entrer l'adresse e-mail pour les alertes: ")
    smtp_server = input("Veuillez entrer l'adresse du serveur SMTP: ")
    smtp_port = int(input("Veuillez entrer le port du serveur SMTP: "))
    smtp_username = input("Veuillez entrer votre nom d'utilisateur SMTP: ")
    smtp_password = getpass.getpass("Veuillez entrer votre mot de passe SMTP: ")

def send_email_alert(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = alert_email 

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
    except smtplib.SMTPAuthenticationError as e:
        if "Username and Password not accepted" in str(e):
            print("Erreur d'authentification: Nom d'utilisateur ou mot de passe incorrect.")
        else:
            print(f"Erreur d'authentification SMTP: {e}")
    except smtplib.SMTPException as e:
        print(f"Erreur SMTP: {e}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")

def monitor_resources():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        update_gui(cpu_usage, memory_usage, disk_usage)

        if send_email_alerts:
            if cpu_usage > CPU_THRESHOLD:
                send_email_alert('CPU Alert', f'CPU usage is {cpu_usage}%')
            if memory_usage > MEMORY_THRESHOLD:
                send_email_alert('Memory Alert', f'Memory usage is {memory_usage}%')
            if disk_usage > DISK_THRESHOLD:
             send_email_alert('Disk Alert', f'Disk usage is {disk_usage}%')

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

    # Changer la couleur des graphiques si les seuils sont dépassés
    if cpu > CPU_THRESHOLD:
        ax_cpu.set_facecolor('red')
    else:
        ax_cpu.set_facecolor('white')
        
    if memory > MEMORY_THRESHOLD:
        ax_memory.set_facecolor('red')
    else:
        ax_memory.set_facecolor('white')
        
    if disk > DISK_THRESHOLD:
        ax_disk.set_facecolor('red')
    else:
        ax_disk.set_facecolor('white')

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

print("Appuyez sur Ctrl+C pour quitter l'interface.")

threading.Thread(target=monitor_resources, daemon=True).start()

root.mainloop()
