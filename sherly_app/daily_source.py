#--------------------------------------------------------
import os
import sys
import logging
import datetime
import subprocess
from django.conf import settings
from django.core.mail import EmailMessage
import time

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))
# Set the path to the log file
log_file_path = os.path.join(script_directory, 'daily_source.log')

# Configure logging to write to the log file
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add the directory containing the Django project to the Python path
project_root = os.path.abspath(os.path.join(script_directory, '..'))
sys.path.append(project_root)

# Set the Django settings module environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SHERLY.settings")

# Manually configure Django settings
import django
django.setup()
from django.core.mail import EmailMessage
from sherly_app.models import EmailSettings, Societe
from django.template.loader import render_to_string
import shutil


def create_backup():
    try:
        # Définir le chemin du dossier source
        source_folder = '/home/sherylstrategy/RECO/SHERLYY'
        # Définir le chemin du dossier temporaire
        temp_folder = '/tmp/backup_source'

        # Créer le dossier temporaire s'il n'existe pas
        os.makedirs(temp_folder, exist_ok=True)

        # Copier le contenu du dossier source vers le dossier temporaire
        for item in os.listdir(source_folder):
            item_path = os.path.join(source_folder, item)
            if os.path.isfile(item_path):
                shutil.copy(item_path, temp_folder)
            elif os.path.isdir(item_path):
                shutil.copytree(item_path, os.path.join(temp_folder, item))

        logging.info("La copie du contenu du dossier source est terminée avec succès.")

        return temp_folder  # Retourne le chemin du dossier temporaire
    except Exception as e:
        logging.error(f"Une erreur inattendue s'est produite lors de la création de la sauvegarde : {str(e)}")
        return None  # Retourne None si la sauvegarde échoue

if __name__ == "__main__":
    backup_folder_path = create_backup()

    if backup_folder_path:
        # Journaliser le chemin du dossier de sauvegarde
        logging.info(f"Chemin du dossier de sauvegarde : {backup_folder_path}")

        # Pause de 5 secondes
        time.sleep(10)

        # Vérifier si le dossier de sauvegarde existe
        if os.path.exists(backup_folder_path):
            logging.info(f"Le dossier de sauvegarde existe à l'emplacement : {backup_folder_path}")
            email_settings = EmailSettings.objects.first()
            if email_settings:
                # Affecter chaque champ à une variable
                email_backend = email_settings.EMAIL_BACKEND
                email_host = email_settings.EMAIL_HOST
                email_host_user = email_settings.EMAIL_HOST_USER
                email_host_password = email_settings.EMAIL_HOST_PASSWORD
                email_port = email_settings.EMAIL_PORT
                email_use_tls = email_settings.EMAIL_USE_TLS
                default_from_email = email_settings.DEFAULT_FROM_EMAIL
                server_email = email_settings.SERVER_EMAIL
            # Définir les paramètres de messagerie électronique dynamiquement
            settings.EMAIL_BACKEND = email_backend
            settings.EMAIL_HOST = email_host
            settings.EMAIL_HOST_USER = email_host_user
            settings.EMAIL_HOST_PASSWORD = email_host_password
            settings.EMAIL_PORT = email_port
            settings.EMAIL_USE_TLS = email_use_tls
            settings.DEFAULT_FROM_EMAIL = default_from_email
            settings.SERVER_EMAIL = server_email
            societe = Societe.objects.first()

            subject = "BACKUP SOURCE CODE"
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            message = f"BACKUP SOURCE CODE FOR: {current_time}."
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [societe.boite_reception, "salmi.ensa.ilsi@gmail.com"]  # Mettez à jour avec votre liste de destinataires
            email = EmailMessage(subject, message, from_email, recipient_list)

            # Attacher les fichiers du dossier de sauvegarde à l'e-mail
            try:
                for item in os.listdir(backup_folder_path):
                    item_path = os.path.join(backup_folder_path, item)
                    if os.path.isfile(item_path):
                        with open(item_path, "rb") as attachment:
                            # Journaliser l'attachement du fichier
                            logging.info(f"Attacher le fichier : {item_path}")
                            # Attacher le fichier à l'e-mail
                            email.attach(item, attachment.read())
                    elif os.path.isdir(item_path):
                        for root, dirs, files in os.walk(item_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                with open(file_path, "rb") as attachment:
                                    # Journaliser l'attachement du fichier
                                    logging.info(f"Attacher le fichier : {file_path}")
                                    # Attacher le fichier à l'e-mail
                                    email.attach(file, attachment.read())

            except Exception as e:
                # Journaliser les erreurs lors de l'attachement des fichiers
                logging.error(f"Une erreur s'est produite lors de l'attachement des fichiers : {str(e)}")

            # Envoyer l'e-mail
            try:
                logging.info("Envoi de l'e-mail...")
                email.send()
                logging.info("Email envoyé avec succès.")

                # Supprimer les fichiers temporaires après l'envoi de l'e-mail
                shutil.rmtree(backup_folder_path)
                logging.info(f"Fichiers temporaires supprimés avec succès : {backup_folder_path}")
            except Exception as e:
                # Journaliser les erreurs lors de l'envoi de l'e-mail
                logging.error(f"Une erreur s'est produite lors de l'envoi de l'e-mail : {str(e)}")
        else:
            logging.error(f"Le dossier de sauvegarde n'existe pas à l'emplacement : {backup_folder_path}")