from django.apps import apps
from django.core.management.base import CommandError
# from dataentry.models import Student
from django.apps import apps
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import os
import datetime

def get_all_custom_models():
    default_models = ['ContentType','Session','LogEntry','Group','Permission','User','Upload']
    #try to get all the apps
    custom_models = []
    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
    # print(custom_models)
    return custom_models


# import data command ( error logic + get model without any erro ) logic 
def check_csv_errors(file_path, model_name):
    
    model = None

    # Search for the model across all installed apps
    for app_config in apps.get_app_configs():
        # Try to search for model
        try:
            # It looks for the model class named 'ModelName' inside the app with label 'app_label'.
            # If Django finds the model, it returns a real model class — e.g., <class 'dataentry.models.Student'>
            model = apps.get_model(app_config.label, model_name)
            break
        except LookupError:
            continue #model not found in this app, continue searching in next app.

    if not model:
        raise CommandError(f"Model {model_name} not found in any app!")
    
    # get all teh field names of the model that we found 
    model_fields = [field.name for field in model._meta.fields if field.name!= 'id']

    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file) #It reads CSV rows as dictionaries, where:Keys are taken from the header row (first line in CSV), Values are the remaining row values,this takes first row as fieldsname
            csv_header = reader.fieldnames

            # compare csv header with model's field names
            if csv_header != model_fields:
                raise DataError(f"CSV file doesn't match with the {model_name} table fields")
            
    except Exception as e:
        raise e
    
    return model


def send_email_notification(mail_subject, message, to_email, attachment=None):
    try: 
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        if attachment is not None:
            mail.attach_file(attachment)
        mail.send()
    except Exception as e:
        raise e

def generate_csv_file(model_name):
    # generate the timestamp of current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # define the csv file name/path

    export_dir = 'exported_data'
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    return file_path