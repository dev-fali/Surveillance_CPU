import psutil
import smtplib
from email.mime.text import MIMEText
from slack_sdk import WebClient

# Définition des seuils pour les alertes
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 80


def send_email_alert(subject, message):
    # Configurer les paramètres SMTP
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_username = 'your_username'
    smtp_password = 'your_password'

    # Créer le message MIME
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = 'alert@example.com'
    msg['To'] = 'admin@example.com'

    # Établir une connexion SMTP et envoyer le message
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

# Fonction pour envoyer des alertes sur Slack
def send_slack_alert(message):
    # Initialiser le client Slack
    client = WebClient(token='your_slack_token')

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

