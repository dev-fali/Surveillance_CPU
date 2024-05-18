import psutil
import smtplib
from email.mime.text import MIMEText
from slack_sdk import WebClient
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv(dotenv_path='.env/data.env')

# Définition des seuils
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 80

def send_email_alert(subject, message):
    # Configurer les paramètres SMTP à partir des variables d'environnement
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = 587
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')

    # Créer le message MIME
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = 'adresse mail'

    # Établir une connexion SMTP et envoyer le message
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

# Fonction pour envoyer des alertes sur Slack
def send_slack_alert(message):
    # Initialiser le client Slack à partir des variables d'environnement
    slack_token = os.getenv('SLACK_TOKEN')
    client = WebClient(token=slack_token)

    # Envoyer le message à un canal Slack spécifié
    response = client.chat_postMessage(channel='#alerts', text=message)

def check_resources():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    if cpu_usage > CPU_THRESHOLD:
        send_email_alert('CPU Alert', f'CPU usage is {cpu_usage}%')
        send_slack_alert(f'CPU usage is {cpu_usage}%')
    if memory_usage > MEMORY_THRESHOLD:
        send_email_alert('Memory Alert', f'Memory usage is {memory_usage}%')
        send_slack_alert(f'Memory usage is {memory_usage}%')
    if disk_usage > DISK_THRESHOLD:
        send_email_alert('Disk Alert', f'Disk usage is {disk_usage}%')
        send_slack_alert(f'Disk usage is {disk_usage}%')

check_resources()