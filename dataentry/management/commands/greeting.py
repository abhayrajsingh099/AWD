from django.core.management.base import BaseCommand


# Proposed command = py manage.py greeting Name(dynamic)
# Proposed output = Hello Name, Good Morning
class Command(BaseCommand):
    help = "Greets user"

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Specifies user name')

    def handle(self, *args, **kwargs): # args = non-keyword arguments, kwargs = keyword arguments (like 'name': 'Abhay')
        # write the logic 
        name = kwargs['name']
        greeting = f"Hello {name}, Good Morning"
        self.stdout.write(self.style.SUCCESS(greeting))