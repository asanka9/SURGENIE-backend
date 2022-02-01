from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=50)

    # TODO insert role choice
    # TODO insert hospital 1:M relationship


class Developer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)


class Surgeon(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=50)
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

    # TODO insert surgeon 1:M relationship


class TraineeSurgeon(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

    # TODO experience? uni? specialty?


class Anesthesiologist(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    registration_number = models.CharField(max_length=20)

    # TODO user 1:1?
    # TODO Insert hospital 1:M relationship


class Nurse(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    registration_number = models.CharField(max_length=20)
    is_sister = models.BooleanField() # Sister is the main nurse

    # TODO user 1:1? experience? hospital relationship?


class TraineeSurgeonSession(models.Model):
    pass
    # TODO trainee surgeon session?


class Admin(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    telephone = models.CharField(max_length=10)
    designation = models.CharField(max_length=30)
    level = models.IntegerField()
    address = models.CharField(max_length=200)

    # TODO insert hospital 1:M relationship

