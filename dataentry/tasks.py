from awd_main.celery import app
import time
from django.core.management import call_command
# from django.core.mail import EmailMessage
from django.conf import settings
from .utils import send_email_notification

@app.task
def celery_test_task():
    # time.sleep(10) # simulation of any task that's going to take 10 seconds
    # send an email
    mail_subject = 'Test subject' 
    message = 'This is from django a test email huraayy everything is interesting learn brrohh ✅✅'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject,message,to_email)


@app.task
def import_data_task(file_path, model_name):
    # Trigger the import-data command
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e
    
    # notify the user by email
    mail_subject = 'Import Data Completed'
    message = f"Your Data has been imported successfully in {model_name} Model"
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject,message,to_email)

    
    return "Data imported Successfully."
        
    