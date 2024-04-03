import os
import django
from django.conf import settings
import subprocess

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SHERLY.settings')

# Load Django settings
django.setup()

try:
    # Access Django settings
    password = settings.NIGHT

    # Define other variables
    backup_path = "amnzo_backup.sql"

    # Define the command to execute
    command = [
        "mysqldump",
        "-u", "sherylstrategy",
        f"-p{password}",
        "-h", "sherylstrategy.mysql.pythonanywhere-services.com",
        "--single-transaction",
        "--no-tablespaces",
        "--column-statistics=0",
        "sherylstrategy$default"
    ]

    # Execute the command using subprocess
    with open(backup_path, "w") as backup_file:
        subprocess.run(command, stdout=backup_file, check=True)

    print("La sauvegarde de la base de données est terminée avec succès.")
except subprocess.CalledProcessError as e:
    print(f"Échec de la sauvegarde de la base de données : {str(e)}")
except Exception as e:
    print(f"Une erreur inattendue s'est produite : {str(e)}")
