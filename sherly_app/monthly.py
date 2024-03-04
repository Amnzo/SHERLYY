import os
import sys
import logging

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

# Now you can import and use your Django models and settings
from SHERLY.settings import PDFKIT_CONFIG
from django.core.mail import EmailMessage
from sherly_app.models import Bon_Livraison, Facture, Societe
from django.template.loader import render_to_string
import pdfkit
from datetime import datetime, timedelta
from django.utils import timezone
import calendar
import base64

logging.info("---------------Starting fetching data to send by email Montly-----------------")
logging.info("---------------PREPARATION FACTURE-----------------")



def envoyer_facture():
    current_date = timezone.now()
    year = current_date.year
    month = current_date.month
    num_days_in_month = calendar.monthrange(year, month)[1]
    if current_date.day == num_days_in_month :
        facture = Facture.objects.first()
        societe = Societe.objects.first()
        first_day = timezone.datetime(year, month, 1)  # First day of the month
        last_day = current_date  # Last day of the month is today
        bons_livraison = Bon_Livraison.objects.filter(date_de_bl__range=(first_day, last_day))
        formatted_date = current_date.strftime("%Y%m%d")
        numero_facture = int(formatted_date)+90
        with open(societe.logo.path, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        context = {
        'bons_livraison':bons_livraison,
        'logo_base64':logo_base64,
        'societe': societe,
        'num_facture':numero_facture,
        'date_facture':current_date,
        'facture':facture
        }
        html = render_to_string('facture/telechargement_facture.html', context)
        config = pdfkit.configuration(wkhtmltopdf=PDFKIT_CONFIG['wkhtmltopdf'])
        pdf = pdfkit.from_string(html, False, options={'encoding': 'UTF-8', 'disable-javascript': None, 'enable-local-file-access': ''}, configuration=config)

        subject = f'Facture du {year}-{month}'
        message = f'Bonjour,  Facture numero {numero_facture} envoyé depuis  SHERYL & STRATEGY SL.'
        #message = f'Bonjour, Ceci est un Bon de Livraison numero {bon_livraison.no_bl} envoyé depuis Django au 6eme café.'
        from_email = societe.boite_envoi
        recipient_list = ['salmi.ensa.ilsi@gmail.com', societe.boite_reception]
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.attach(f'Facture_{numero_facture}.pdf', pdf, 'application/pdf')
        email.send()
        



envoyer_facture()
