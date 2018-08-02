from django.contrib import admin

from product.models import ProductCode, ProductLine, Batch, CodeCollection


class ProductLineAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'manufacturer', 'description', 'photo')
    list_filter = ['is_active', 'manufacturer']
    search_fields = ['product_name', ]


class ProductCodeAdmin(admin.ModelAdmin):
    pass


class BatchAdmin(admin.ModelAdmin):
    pass


class CodeCollectionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Batch, BatchAdmin)
admin.site.register(CodeCollection, CodeCollectionAdmin)
admin.site.register(ProductCode, ProductCodeAdmin)
admin.site.register(ProductLine, ProductLineAdmin)
