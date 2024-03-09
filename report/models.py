from django.db import models

# Create your models here.


class Patient(models.Model):
    clinic_name = models.CharField(max_length=255)
    clinic_logo = models.ImageField(upload_to='clinic_logos/')
    physician = models.CharField(max_length=255)
    physician_contact = models.CharField(max_length=20)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField()
    contact = models.CharField(max_length=20)
    chief_complaint = models.TextField()
    consultation_note = models.TextField()
