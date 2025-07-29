from django.core.management.base import BaseCommand,CommandError
# from dataentry.models import Student
from django.apps import apps
import csv
from django.db import DataError
# Proposed command - python manage.py import data file_path model_name


class Command(BaseCommand):
    help = 'Import data from CSV file'

    def add_arguments(self, parse):
        parse.add_argument('file_path', type=str, help='Path to the CSV file')
        parse.add_argument('model_name', type=str, help='Name of the Model')

    def handle(self, *args, **kwargs):
        #logic goes here
        file_path = kwargs['file_path']
        model_name =  kwargs['model_name'].capitalize()

        # Search for the model across all installed apps
        model = None
        for app_config in apps.get_app_configs():
            # Try to search for model
            try:
                # It looks for the model class named 'ModelName' inside the app with label 'app_label'.
                # If Django finds the model, it returns a real model class — e.g., <class 'dataentry.models.Student'>
                model = apps.get_model(app_config.label, model_name)
                break # once model is found
            except LookupError:
                continue #model not found in this app, continue searching in next app.
        
        if not model:
            raise CommandError(f"Model '{model_name}' not found in any app!")
        
        
        # get all teh field names of the model that we found 
        model_fields = [field.name for field in model._meta.fields if field.name != 'id']
        print(model_fields)


        with open(file_path,'r' ) as file:
            reader = csv.DictReader(file) #It reads CSV rows as dictionaries, where:Keys are taken from the header row (first line in CSV), Values are the remaining row values,this takes first row as fieldsname
            csv_header = reader.fieldnames

            # compare csv header with model's field names
            if csv_header != model_fields:
                raise DataError(f"CSV file doesn't match with the {model_name} table fields")

            for row in reader:
                model.objects.create(**row) # **row includes all row dynamically
        self.stdout.write(self.style.SUCCESS("Data imported and inserted succesfully"))