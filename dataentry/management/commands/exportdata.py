from django.core.management.base import BaseCommand,CommandError
import csv
# from dataentry.models import Student
import datetime
from django.apps import apps

# proposed command = python manage.py exportdata Model_name/Table_name
class Command(BaseCommand):
    help = 'Export data from the database to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Inputs Model_name')

    def handle(self, *args, **kwargs):
        
        model_name = kwargs['model_name'].capitalize()

        # Search for model in all apps
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                pass

        if not model:
            self.stderr.write(f"Model {model_name} could not found")
            return 
        
        #fetch data from database
        data = model.objects.all()

        #generate timestamp of current date and time
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        
        #define the csv file name/path
        file_path = f"exported_{model_name}_data_{timestamp}.csv"

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            #write the csv header
            # we want to print the field names of the model that we are trying to export
            writer.writerow([field.name for field in model._meta.fields])

            for dt in data: #dt for loops works as a column, whereas, getattr(dt,field.name) works as row for loop-> [getattr(dt, 'id'), getattr(dt, 'name'), getattr(dt, 'age')]
                writer.writerow([getattr(dt, field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS('Data exported successfully!'))
