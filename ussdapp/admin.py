from django.contrib import admin

# Register your models here.
from ussdapp.models import UssdRecord


class UssdRecordAdmin(admin.ModelAdmin):
    pass


admin.site.register(UssdRecord, UssdRecordAdmin)
