from django.contrib import admin

from accounts.models import Manufacturer, Location, Profile


# Register your models here.
class ManufacturerAdmin(admin.ModelAdmin):
    pass


class LocationAdmin(admin.ModelAdmin):
    pass


class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
