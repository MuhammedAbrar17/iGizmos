from django.contrib import admin
from .models import AdminCategory,Brand


# Register your models here.
class categoryadmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',) }
    list_display = ("category_name",'slug')
admin.site.register(AdminCategory,categoryadmin)
admin.site.register(Brand)