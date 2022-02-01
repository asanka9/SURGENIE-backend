from django.db import models


class BookedResource(models.Model):
    start_minute = models.IntegerField()
    end_minute = models.IntegerField()
    start_hour = models.IntegerField()
    end_hour = models.IntegerField()
    date = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    day = models.DateField()

    # TODO resource 1:M relationship


class BookedSurgeon(models.Model):
    start_minute = models.IntegerField()
    end_minute = models.IntegerField()
    start_hour = models.IntegerField()
    end_hour = models.IntegerField()
    date = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    day = models.DateField()

    # TODO surgeon 1:M relationship


class BookedTraineeSurgeon(models.Model):
    start_minute = models.IntegerField()
    end_minute = models.IntegerField()
    start_hour = models.IntegerField()
    end_hour = models.IntegerField()
    date = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    day = models.DateField()

    # TODO trainee 1:M relationship


class BookedNurse(models.Model):
    start_minute = models.IntegerField()
    end_minute = models.IntegerField()
    start_hour = models.IntegerField()
    end_hour = models.IntegerField()
    date = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    day = models.DateField()

    # TODO nurse 1:M relationship

