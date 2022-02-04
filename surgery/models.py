from django.db import models
from user.models import Surgeon
from hospital.models import Resource


class Surgery(models.Model):
    name = models.CharField(max_length=150)
    start_minute = models.IntegerField()
    end_minute = models.IntegerField()
    start_hour = models.IntegerField()
    end_hour = models.IntegerField()
    start_date = models.IntegerField()
    end_date = models.IntegerField()
    start_day = models.DateField()
    end_day = models.DateField()
    month = models.IntegerField()  # Int or char?
    year = models.IntegerField()
    notes = models.TextField()

    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)
    # TODO surgeon 1:M relationship


class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    telephone = models.CharField(max_length=10)
    age = models.IntegerField()
    gender = models.IntegerField()
    weight = models.IntegerField()
    height = models.IntegerField()
    cancer = models.IntegerField()
    cvd = models.IntegerField()
    dementia = models.IntegerField()
    diabetes = models.IntegerField()
    digestive = models.IntegerField()
    osteoarthritis = models.IntegerField()
    pylogical = models.IntegerField()
    pulmonary = models.IntegerField()

    surgery = models.ForeignKey(Surgery, on_delete=models.CASCADE)
    # TODO insert surgery 1:M relationship


class SurgeryResource(models.Model):
    amount = models.IntegerField()

    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    # TODO insert 1:M surgery, resource relationships

