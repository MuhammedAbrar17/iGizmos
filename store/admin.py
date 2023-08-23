from django.contrib import admin
from .models import product,ProductVariant


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','category','modified_date','is_available')
    prepopulated_fields = {'slug' : ('product_name',)}
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','quantity','price','ram','storage')

admin.site.register(product)
admin.site.register(ProductVariant,VariationAdmin)
