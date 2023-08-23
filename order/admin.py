from django.contrib import admin
from .models import PaymentMethod
from .models import OrderItem
# Register your models here.
admin.site.register(PaymentMethod)
admin.site.register(OrderItem)