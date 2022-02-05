from django.contrib import admin

# Register your models here.
from booked.models import BookedNurse, BookedSurgeon, BookedTraineeSurgeon, BookedAnesthesiologist

admin.site.register(BookedNurse)
admin.site.register(BookedSurgeon)
admin.site.register(BookedTraineeSurgeon)
admin.site.register(BookedAnesthesiologist)