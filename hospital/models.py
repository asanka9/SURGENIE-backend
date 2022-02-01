from django.db import models


class Hospital(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    telephone = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    trial_period = models.IntegerField()
    installed_date = models.DateField()

    # TODO insert relationship


class Theater(models.Model):
    name = models.CharField(max_length=30)
    number = models.IntegerField()

    # TODO hospital 1:M relationship


class Resource(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    amount = models.IntegerField()
    availability = models.BooleanField()

    # TODO insert unit choices


class SurgeryClick(models.Model):
    predicted_value = models.IntegerField()
    estimated_value = models.IntegerField()

    # TODO resource type choices
    # TODO hospital 1:M relationship


class Model(models.Model):
    location = models.CharField(max_length=50)

    # TODO surgery type choices?
    # TODO hospital 1:M relationship


