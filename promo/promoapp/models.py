from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, RegexValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True,
                            validators=[RegexValidator(
                                "^[A-Z0-9]*$", "code enter must be uppercase letters & numbers",
                            )], null=True, blank=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),)
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES)
    def start_dates(start):
        sd = timezone.now()
        if start < sd:
            raise ValidationError('enter current date..')

    def end_dates(end):
        ed = timezone.now()
        if end < ed:
            raise ValidationError('enter future date....')

    start_date = models.DateTimeField(validators=[start_dates])
    end_date = models.DateTimeField(validators=[end_dates])
    discount = models.IntegerField(default=None, validators=[MaxValueValidator(100)])

    TYPE_CHOICES = [('flat', 'Flat'),
                    ('Percentage', 'percentage')]

    discounttype = models.CharField(choices=TYPE_CHOICES, default='Flat', max_length=10)
    max_coupen = models.IntegerField(null=True)
    user_limit = models.IntegerField(null=True)


    def clean(self):
        super().clean()
        if not (self.start_date <= self.end_date):
            raise ValidationError("Don't select Invalid start and end date")

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        return super(Coupon, self).save(*args, **kwargs)

    def __str__(self):
        return self.code


class UserData(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return "{}".format(self.username)


class Order(models.Model):
    order_amount = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(1500000)])
    user = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='order_user')
    order_total = models.IntegerField()
    order_coupen = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='my_coupen')
    used = models.IntegerField(default=0)
