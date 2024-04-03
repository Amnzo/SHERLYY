
import os
import sys
import logging
from datetime import timedelta
import calendar
from decimal import Decimal
import base64
import tempfile
import PyPDF2
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import pdfkit
from django.conf import settings

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))
# Set the path to the log file
log_file_path = os.path.join(script_directory, 'monthly_5.log')

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
from sherly_app.models import Bon_Livraison, Facture, Societe,EmailSettings,Invoice
from django.template.loader import render_to_string
import pdfkit
from django.utils import timezone
import calendar
import base64
import tempfile
from django.conf import settings  # Add this import statement
from decimal import Decimal
import PyPDF2
logging.info("---------------Starting fetching data to send by email Montly-----------------")
logging.info("---------------PREPARATION FACTURE for  end+5-----------------")
from django.conf import settings

logging.basicConfig(filename='monthly_5.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def envoyer_facture():
    current_date = timezone.now()
    next_month = current_date.replace(day=5) + timedelta(days=30)
    logging.info("next_month")
    logging.info(next_month)

    if current_date.day ==5 :
        last_month = current_date - timedelta(days=current_date.day)
        logging.info(f" current_date={current_date} ")
        logging.info(f"{current_date} - {timedelta(days=current_date.day)}={last_month}")
        logging.info(f"last_month is = {last_month}")
        logging.info(last_month)

        first_day_last_month = last_month.replace(day=1)
        logging.info("first_day_last_month = {first_day_last_month} ")
        last_day_last_month = last_month.replace(day=calendar.monthrange(last_month.year, last_month.month)[1])
        logging.info(f"last_day_last_month={last_day_last_month}")

        bons_livraisons = Bon_Livraison.objects.filter(
            date_de_bl__range=(first_day_last_month, last_day_last_month),
            bon_commande__is_active=True
        )
        logging.info(f"RESULTAT DE LA FACTURE={bons_livraisons}")

        logging.info(bons_livraisons)

        sub_total_1=Decimal(0)
        for bon_livraison in bons_livraisons:
            sub_total_1 += (bon_livraison.bon_commande.produit_d.prix * bon_livraison.bon_commande.quatite_d) + (bon_livraison.bon_commande.produit_g.prix * bon_livraison.bon_commande.quatite_g)

        logging.info(f"TOTAL  DE LA FACTURE={round(sub_total_1, 2)}")
        societe = Societe.objects.first()
        facture = Facture.objects.first()
        #societe = Societe.objects.first()
        tva_value = Decimal(0)
        remise_value = Decimal(0)
        sub_total_1 = round(sub_total_1, 2)
        sub_total_2=round(sub_total_1, 2)
        if societe.remise != 0:
            remise_value = Decimal(societe.remise) / 100
        if remise_value != Decimal(0):
            remise_value = sub_total_1 * remise_value
            remise_value=round(remise_value, 2)
            sub_total_2=sub_total_2-remise_value

        if societe.tva != 0:
            tva_value = Decimal(societe.tva) / 100

        if tva_value != Decimal(0):
            tva_value = sub_total_2 * tva_value
            total_ttc = sub_total_2 + tva_value
            tva_value = round(tva_value, 2)
            total_ttc = round(total_ttc, 2)
        else:
            total_ttc = sub_total_2

        formatted_date = current_date.strftime("%Y%m%d")
        month_year = last_day_last_month.strftime("%m-%Y")
        logging.info("periode----------")
        logging.info(month_year)
        existing_invoice = Invoice.objects.filter(mois_concerne=month_year).first()
        if not existing_invoice:
                logging.info("INVOICE EXISTE")
                date_part = month_year.replace("-", "")
                last_invoice = Invoice.objects.last()
                padded_id = f"{(last_invoice.id * last_invoice.id) + last_invoice.id}" if last_invoice else "1"
                invoice_number = f"{date_part}{padded_id}"
                new_invoice = Invoice.objects.create(
                invoice_number=invoice_number,
                mois_concerne=month_year)
                numero_facture = new_invoice.invoice_number
                #invoice_id=new_invoice.id
        else :
                logging.info("CREATEING NEW INVOICE ")
                numero_facture = existing_invoice.invoice_number
                #invoice_id=existing_invoice.id


        #numero_facture = int(formatted_date) + 90

        with open(societe.logo.path, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        context = {
            'bons_livraison': bons_livraisons,
            'logo_base64': logo_base64,
            'societe': societe,
            'facture':facture,
            'num_facture': numero_facture,
            #'date_facture': current_date.strftime("%d-%m-%Y"),
            'date_facture':last_day_last_month.strftime("%d-%m-%Y"),
            'total_': sub_total_1,
            'total__': sub_total_2,
            'remise': remise_value,
            'tva': tva_value,
            'total_ttc': total_ttc,
        }

        html = render_to_string('facture/telechargement_facture.html', context)
        config = pdfkit.configuration(wkhtmltopdf=PDFKIT_CONFIG['wkhtmltopdf'])
        pdf = pdfkit.from_string(html, False, options={'encoding': 'UTF-8', 'disable-javascript': None, 'enable-local-file-access': ''}, configuration=config)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(pdf)
            temp_file.seek(0)
            file_path = temp_file.name

            writer = PyPDF2.PdfFileWriter()
            reader = PyPDF2.PdfFileReader(file_path)
            for page_num in range(reader.numPages):
                writer.addPage(reader.getPage(page_num))

            writer.encrypt('', societe.pdf_pwd, 0, True)
            with open(file_path + '_secured.pdf', 'wb') as output_file:
                writer.write(output_file)

        email_settings = EmailSettings.objects.first()
        logging.info(f"email_settings= {email_settings}")
        if email_settings:
            email_backend = email_settings.EMAIL_BACKEND
            email_host = email_settings.EMAIL_HOST
            email_host_user = email_settings.EMAIL_HOST_USER
            email_host_password = email_settings.EMAIL_HOST_PASSWORD
            email_port = email_settings.EMAIL_PORT
            email_use_tls = email_settings.EMAIL_USE_TLS
            default_from_email = email_settings.DEFAULT_FROM_EMAIL
            server_email = email_settings.SERVER_EMAIL

        settings.EMAIL_BACKEND = email_backend
        settings.EMAIL_HOST = email_host
        settings.EMAIL_HOST_USER = email_host_user
        settings.EMAIL_HOST_PASSWORD = email_host_password
        settings.EMAIL_PORT = email_port
        settings.EMAIL_USE_TLS = email_use_tls
        settings.DEFAULT_FROM_EMAIL = default_from_email
        settings.SERVER_EMAIL = server_email

        subject = f'Factura del {last_month.strftime("%Y-%m")}'
        message = ""
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [societe.boite_reception,"salmi.ensa.ilsi@gmail.com"]
        logging.info(f" societe.boite_reception= {societe.boite_reception}")

        email = EmailMessage(subject, message, from_email, recipient_list)
        secured_pdf_file = open(file_path + '_secured.pdf', 'rb')
        email.attach(f'FACTURA_Nº_{numero_facture}.pdf', secured_pdf_file.read(), 'application/pdf')
        email.send()
    else:
        logging.info("Today is not the scheduled day for sending invoices.")

envoyer_facture()
