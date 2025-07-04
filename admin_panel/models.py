from django.db import models

FARE_TYPE_CHOICES = [
    ('boys', 'Boys'),
    ('vice_supervisor', 'Vice Supervisor'),
    ('supervisor', 'Supervisor'),
    ('captain', 'Captain'), 
    ('setting', 'Setting'),
    ('loading', 'Loading'),
]

class BaseFare(models.Model):
    fare_type = models.CharField(max_length=30, choices=FARE_TYPE_CHOICES,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.get_fare_type_display()} - ₹{self.amount}"