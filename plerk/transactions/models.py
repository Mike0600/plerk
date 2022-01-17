#Django
from enum import Flag
from time import timezone
from django.db import models
from django.contrib.auth.models import User




class Company(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_STATUS_OPTIONS = [
        ('C', 'closed'),
        ('R','reversed'),
        ('P', 'pending'),
    ]

    company_id = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='Company name') 

    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    transaction_status = models.CharField(max_length=1, choices=TRANSACTION_STATUS_OPTIONS)
    approbal_status = models.BooleanField(default=False)
    final_charge = models.BooleanField(default=False)


