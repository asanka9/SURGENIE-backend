from django.db import models
from hospital.models import Hospital


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=50)

    ROLES = [
        ('admin', 'Administrator'),
        ('surgeon', 'Surgeon'),
        ('trainee_surgeon', 'Trainee Surgeon'),
        ('nurse', 'Nurse'),
    ]

    role = models.CharField(max_length=50, choices=ROLES)

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True)
    # TODO insert hospital 1:M relationship

    class Meta:
        abstract = True


class Developer(User):
    role = models.CharField(max_length=50, default='dev')

    # TODO insert user 1:1 relationship


class Surgeon(User):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     address = models.CharField(max_length=200)
#     email = models.EmailField(max_length=50)
    specialty = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=20)
    experience = models.TextField()  # Experience describe the past works

    # TODO Hospital 1:M relationship
    # TODO User relationship?


class SurgeonSession(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_day = models.IntegerField()  # Int or DateField()?
    end_day = models.IntegerField()

    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)
    # TODO insert surgeon 1:M relationship


class TraineeSurgeon(User):
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # email = models.EmailField(max_length=50)
    registration_number = models.CharField(max_length=20)
    experience = models.TextField()
    # TODO experience? hospital? specialty?


class Anesthesiologist(User):
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # email = models.EmailField(max_length=50)
    registration_number = models.CharField(max_length=20)

    # TODO user 1:1?
    # TODO Insert hospital 1:M relationship


class Nurse(User):
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # email = models.EmailField(max_length=50)
    registration_number = models.CharField(max_length=20)
    is_sister = models.BooleanField() # Sister is the main nurse

    # TODO experience? hospital relationship?


class TraineeSurgeonSession(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_day = models.IntegerField()  # Int or DateField()?
    end_day = models.IntegerField()

    trainee_surgeon = models.ForeignKey(TraineeSurgeon, on_delete=models.CASCADE)
    # TODO trainee surgeon session?


class Admin(User):
    telephone = models.CharField(max_length=10)
    designation = models.CharField(max_length=30)
    level = models.IntegerField()

    # TODO insert hospital 1:M relationship
    # TODO user relationship?


class Quote(models.Model):
    quote = models.TextField()

    ROLES = [
        ('admin', 'Administrator'),
        ('surgeon', 'Surgeon'),
        ('trainee_surgeon', 'Trainee Surgeon'),
        ('nurse', 'Nurse')
    ]

    role = models.CharField(max_length=20, choices=ROLES)
