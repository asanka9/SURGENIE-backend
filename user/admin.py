from django.contrib import admin

# Register your models here.
from user.models import Account, Nurse, Surgeon, TraineeSurgeon, Admin, Anesthesiologist, SurgeonSession, \
    TraineeSurgeonSession

admin.site.register(Account)
admin.site.register(Nurse)
admin.site.register(Surgeon)
admin.site.register(TraineeSurgeon)
admin.site.register(Admin)
admin.site.register(Anesthesiologist)


admin.site.register(SurgeonSession)
admin.site.register(TraineeSurgeonSession)
