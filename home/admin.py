from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(GeneralData)
admin.site.register(CaseData)
admin.site.register(SevereData)
admin.site.register(DeathData)
