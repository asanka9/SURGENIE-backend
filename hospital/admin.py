from django.contrib import admin

# Register your models here.
from hospital.models import Hospital, Resource

admin.site.register(Hospital)
admin.site.register(Resource)