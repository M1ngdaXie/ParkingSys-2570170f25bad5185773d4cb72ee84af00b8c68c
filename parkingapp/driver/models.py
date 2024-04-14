from django.db import models

class Driver(models.Model):

    driver_types = (
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
        ('Guest', 'Guest'),
    )

    driver_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=driver_types)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)


class Vehicle(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    vehicle_id = models.AutoField(primary_key=True)
    license_plate = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    year = models.CharField(max_length=50)


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    credit_card_no = models.CharField(max_length=20) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    check_no = models.CharField(max_length=20, blank=True, null=True)
    cash = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField()


class Violation(models.Model):
    violation_types = (
        ('nopermit', 'No Permit For Lot'),
        ('expiredpermit', 'Expired Permit'),
        ('overnight', 'Overnight Parking'),
    )
    statuses = (
        ('Settled', 'Settled'),
        ('Outstanding', 'Outstanding'),
    )
    violation_id = models.AutoField(primary_key=True)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    violation_types = models.CharField(max_length=50, choices=violation_types, default='nopermit')
    date_issued = models.DateField()
    fine_amount = models.CharField(max_length=20, default='100.00')
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=statuses, default='Outstanding')

from django.utils import timezone
class Permit(models.Model):
     permit_types = (
        ('upermit', 'UPermit'),
        ('cupermit', 'CUPermit'),
        ('apermit', 'APermit'),
        ('daypermit', 'DayPermit'),
    ) 
     status = (
         ('Payed','Payed'),
         ('Not Payed', 'Not Payed'),
     )
     permit_id = models.AutoField(primary_key=True)
     types = models.CharField(max_length=50, choices=permit_types)
     purchase_date = models.DateField()
     expiration_date = models.CharField(max_length=20, default='04/30/2025')
     cost = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
     vehicle_id = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
     driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
     payment_id = models.ForeignKey('Payment', on_delete=models.CASCADE, null=True, blank=True)
     status = models.CharField(max_length=20,choices=status,default='Not Payed')
     amount_due = models.CharField(max_length=20, default='100.00')


