from django.db import models


class Hospital(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    telephone = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    trial_period = models.IntegerField()
    installed_date = models.DateField()


class Theater(models.Model):
    name = models.CharField(max_length=30)
    number = models.IntegerField()

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    # TODO hospital 1:M relationship


class Resource(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    availability = models.BooleanField()

    UNITS = [
        ('ml', 'Milliliters'),
        ('mg', 'Milligrams'),
        ('pcs', 'Pieces'),
        ('unit', 'Units'),
    ]

    unit = models.CharField(max_length=10, choices=UNITS, default=None)
    # TODO insert unit choices



class SurgeryClick(models.Model):
    predicted_value = models.IntegerField()
    estimated_value = models.IntegerField()

    RESOURCE_TYPE = [
        ('drug', 'Drug'),
        ('equipment', 'Equipment'),
    ]

    resource_type = models.CharField(max_length=15, choices=RESOURCE_TYPE)
    # TODO hospital 1:M relationship
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)


class Model(models.Model):
    location = models.CharField(max_length=50)

    # TODO surgery type choices?
    # TODO hospital 1:M relationship


