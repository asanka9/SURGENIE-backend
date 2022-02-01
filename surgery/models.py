from django.db import models


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

    # TODO surgeon 1:M relationship


class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    telephone = models.CharField(max_length=10)

    # TODO insert surgery 1:M relationship


class SurgeryResource(models.Model):
    amount = models.IntegerField()

    # TODO insert 1:M surgery, resource relationships
