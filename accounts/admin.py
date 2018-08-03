from django.contrib import admin

from accounts.models import Manufacturer, Location, Profile, Industry, Position


# Register your models here.

class IndustryAdmin(admin.ModelAdmin):
    pass


class ManufacturerAdmin(admin.ModelAdmin):
    pass


class LocationAdmin(admin.ModelAdmin):
    pass


class ProfileAdmin(admin.ModelAdmin):
    pass


class PositionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
