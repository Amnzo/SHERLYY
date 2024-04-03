# database_backup.py
import os
import sys
import logging
import datetime  # Import datetime module to work with dates
from django.conf import settings
import subprocess
from django.core.mail import EmailMessage

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))
# Set the path to the log file
log_file_path = os.path.join(script_directory, 'daily.log')

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
from sherly_app.models import EmailSettings,Societe
from django.template.loader import render_to_string

def create_backup():
    try:
        # Access database credentials from Django settings
        database_settings = settings.DATABASES['default']
        db_user = database_settings['USER']
        db_password = database_settings['PASSWORD']
        db_host = database_settings['HOST']
        db_name = database_settings['NAME']

        # Define backup file path with the current date in the name
        current_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"backup_{current_date}.sql"  # Set the desired backup file path with date

        # Define the backup command
        command = [
            "mysqldump",
            "-u", db_user,
            f"-p{db_password}",  # Append password securely
            "-h", db_host,
            "--single-transaction",  # Perform a single transaction dump
            "--no-tablespaces",  # Exclude tablespace data
            "--column-statistics=0",  # Disable column statistics
            db_name
        ]

        # Execute the command using subprocess
        with open(backup_path, "w") as backup_file:
            subprocess.run(command, stdout=backup_file, check=True)

        print("Database backup completed successfully.")
        return backup_path  # Return the path of the backup file
    except subprocess.CalledProcessError as e:
        print(f"Database backup failed: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    return None  # Return None if backup fails

def send_email_with_attachment(file_path):
    try:
        email_settings = EmailSettings.objects.first()
        if email_settings:
            # Assign each field to a variable
            email_backend = email_settings.EMAIL_BACKEND
            email_host = email_settings.EMAIL_HOST
            email_host_user = email_settings.EMAIL_HOST_USER
            email_host_password = email_settings.EMAIL_HOST_PASSWORD
            email_port = email_settings.EMAIL_PORT
            email_use_tls = email_settings.EMAIL_USE_TLS
            default_from_email = email_settings.DEFAULT_FROM_EMAIL
            server_email = email_settings.SERVER_EMAIL

        # Set email backend and other settings dynamically
        settings.EMAIL_BACKEND = email_backend
        settings.EMAIL_HOST = email_host
        settings.EMAIL_HOST_USER = email_host_user
        settings.EMAIL_HOST_PASSWORD = email_host_password
        settings.EMAIL_PORT = email_port
        settings.EMAIL_USE_TLS = email_use_tls
        settings.DEFAULT_FROM_EMAIL = default_from_email
        settings.SERVER_EMAIL = server_email
        societe = Societe.objects.first()

        subject = "Backup File"
        current_= datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        message = f" BACKUP database POUR :  {current_}."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [societe.boite_reception,"salmi.ensa.ilsi@gmail.com"]  # Update this with your recipient list
        email = EmailMessage(subject, message, from_email, recipient_list)
        with open(file_path, "rb") as attachment:
            email.attach_file(file_path, 'application/octet-stream')
        email.send()
        os.remove(file_path)
        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred while sending email: {str(e)}")

if __name__ == "__main__":
    backup_file_path = create_backup()
    if backup_file_path:
        send_email_with_attachment(backup_file_path)
