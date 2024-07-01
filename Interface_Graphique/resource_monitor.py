import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv(dotenv_path='.env/data.env')

# Configuration des alertes
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 35
DISK_THRESHOLD = 35

# Fonction pour surveiller les ressources
def monitor_resources():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        update_gui(cpu_usage, memory_usage, disk_usage)
        time.sleep(1)

# Fonction pour mettre à jour l'interface graphique
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

# Création de l'interface graphique principale
root = tk.Tk()
root.title('System Resource Monitor')

cpu_var = tk.StringVar()
memory_var = tk.StringVar()
disk_var = tk.StringVar()

ttk.Label(root, textvariable=cpu_var).pack()
ttk.Label(root, textvariable=memory_var).pack()
ttk.Label(root, textvariable=disk_var).pack()

# Configuration des graphiques
fig, (ax_cpu, ax_memory, ax_disk) = plt.subplots(3, 1, figsize=(6, 6))
cpu_values = []
memory_values = []
disk_values = []

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Lancement du thread de surveillance des ressources
threading.Thread(target=monitor_resources, daemon=True).start()

root.mainloop()
