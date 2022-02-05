from django.db import models

from surgery.models import Surgery
from user.models import Surgeon, Nurse, TraineeSurgeon, Anesthesiologist
from hospital.models import Resource


class Booked(models.Model):
    start_minute = models.IntegerField()
    end_minute = models.IntegerField()
    start_hour = models.IntegerField()
    end_hour = models.IntegerField()
    date = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()

    surgery = models.ForeignKey(Surgery, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class BookedResource(Booked):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    # TODO resource 1:M relationship


class BookedAnesthesiologist(Booked):
    anesthesiologist = models.ForeignKey(Anesthesiologist, on_delete=models.CASCADE)
    # TODO resource 1:M relationship

class BookedSurgeon(Booked):
    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)
    # TODO surgeon 1:M relationship


class BookedTraineeSurgeon(Booked):
    trainee_surgeon = models.ForeignKey(TraineeSurgeon, on_delete=models.CASCADE)
    # TODO trainee 1:M relationship


class BookedNurse(Booked):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    # TODO nurse 1:M relationship

