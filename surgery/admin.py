from django.contrib import admin

# Register your models here.
from surgery.models import Surgery, Patient

admin.site.register(Surgery)
admin.site.register(Patient)
