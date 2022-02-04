from django.db import models

from surgery.models import Surgery
from user.models import Surgeon, Nurse, TraineeSurgeon
from hospital.models import Resource


class Booked(models.Model):
    start_minute = models.IntegerField()
    end_minute = models.IntegerField()
    start_hour = models.IntegerField()
    end_hour = models.IntegerField()
    date = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    day = models.DateField()

    surgery = models.ForeignKey(Surgery, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class BookedResource(Booked):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    # TODO resource 1:M relationship


class BookedSurgeon(Booked):
    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)
    # TODO surgeon 1:M relationship


class BookedTraineeSurgeon(Booked):
    surgeon = models.ForeignKey(TraineeSurgeon, on_delete=models.CASCADE)
    # TODO trainee 1:M relationship


class BookedNurse(Booked):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    # TODO nurse 1:M relationship

