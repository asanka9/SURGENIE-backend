from django.db import models
from user.models import Surgeon, Nurse, Anesthesiologist, TraineeSurgeon


class Fav(models.Model):
    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class FavNurse(Fav):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    # TODO nurse, surgeon 1:M relationship


class FavTraineeSurgeon(Fav):
    trainee_surgeon = models.ForeignKey(TraineeSurgeon, on_delete=models.CASCADE)
    # TODO trainee surgeon, surgeon 1:M relationship


class FavAnesthesiologist(Fav):
    anesthesiologist = models.ForeignKey(Anesthesiologist, on_delete=models.CASCADE)
    # TODO anesthesiologist, surgeon 1:M relationship

