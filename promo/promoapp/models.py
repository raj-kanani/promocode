from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=5, unique=True,
                            validators=[RegexValidator(
                                "^[A-Z0-9]*$", "Only uppercase letters & numbers are allowed.",
                            )], null=True, blank=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),)
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField()
    discount = models.IntegerField(default=None, validators=[MaxValueValidator(100)])

    def clean(self):
        super().clean()
        if not (self.start_date <= self.end_date):
            raise ValidationError('Invalid start and end datetime')

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        return super(Coupon, self).save(*args, **kwargs)


# class User(models.Model):
#     user_id = models.IntegerField()
#     user_birthdate = models.DateField()
#     gender = models.ForeignKey(Coupon, on_delete=models.CASCADE)
#     amount = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(1500000)])


class UserData(AbstractUser):
    birth_date = models.DateField(null=True, blank=False)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return "{}".format(self.username)
