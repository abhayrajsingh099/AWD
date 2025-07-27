from django.core.management.base import BaseCommand
from dataentry.models import Student

# I want to add some data to the database using the custom command

class Command(BaseCommand):
    help = 'It will insert data to the database'

    def handle(self, *args, **kwargs):
        #logic goes here
        # add 1 data
        dataset = [
            {'roll_no':1002,'name':'Sachin', 'age':19},
            {'roll_no':1003,'name':'John', 'age':29},
            {'roll_no':1004,'name':'mick', 'age':22},
            {'roll_no':1005,'name':'bully', 'age':21},
        ]

        for data in dataset:
            roll_no = data['roll_no']
            existing_record = Student.objects.filter(roll_no=roll_no).exists()
            
            if not existing_record:
                Student.objects.create(roll_no=data['roll_no'],name=data['name'],age=data['age'])
            else:
                self.stdout.write(self.style.WARNING(f" {roll_no}'s Data already exists!"))


        self.stdout.write(self.style.SUCCESS('Data inserted successfully !'))