import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parkingapp.settings')

django.setup()

from driver.models import Driver,Permit

# Empties all existing rows from the tables
drivers = Driver.objects.all()
for driver in drivers:
    driver.delete()


# Add drivers to the driver table
Driver.objects.create(
    type ='Student',
    first_name ='Carly',
    last_name ='Anderson',
    address ='12345 Example Rd'
)

Driver.objects.create(
    type ='Student',
    first_name ='Ken',
    last_name ='Haynes',
    address ='653 S 1300 E'
)

Driver.objects.create(
    type ='Faculty',
    first_name ='Matt',
    last_name ='Pecsok',
    address ='69 E 4200 S'
)

