from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

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
    

class BoyRating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role__in': ['boys', 'vice_supervisor', 'supervisor', 'captain']},
        related_name='ratings'
    )

    pant = models.BooleanField(default=False)
    shoe = models.BooleanField(default=False)
    timing = models.BooleanField(default=False)
    neatness = models.BooleanField(default=False)
    performance = models.BooleanField(default=False)

    comment = models.TextField(blank=True, null=True)

    rated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='given_boy_ratings'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def extra_reward(self):
        return sum([
            self.pant,
            self.shoe,
            self.timing,
            self.neatness,
            self.performance
        ]) * 10

    @property
    def base_fare(self):
        try:
            from .models import BaseFare
            fare = BaseFare.objects.get(fare_type=self.user.role)
            return fare.amount
        except ObjectDoesNotExist:
            return 0

    @property
    def total_earning(self):
        return self.base_fare + self.extra_reward

    def __str__(self):
        return f"{self.user.user_name or self.user.email} - ₹{self.total_earning}"
    

class DailyWage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='daily_wages'
    )

    date = models.DateField()
    base_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rating_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    travel_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    over_time = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    long_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    total_wage = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date')

    def calculate_total(self):
        return (
            self.base_fare +
            self.rating_amount +
            self.travel_allowance +
            self.over_time +
            self.long_fare +
            self.bonus
        )

    def save(self, *args, **kwargs):
        self.total_wage = self.calculate_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.user_name or self.user.email} - {self.date} - ₹{self.total_wage}"
