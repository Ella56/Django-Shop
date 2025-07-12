from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    phone_validator = RegexValidator(
        regex=r'^0\d{10}$',
        message='شماره موبایل نامعتبر می باشد.'
        )
    
    phone_number = models.CharField(max_length=11, validators=[phone_validator])
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    content = models.TextField()