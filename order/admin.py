from django.contrib import admin
from .models import PaymentMethod
from .models import OrderItem
from .models import *
# Register your models here.
admin.site.register(PaymentMethod)
admin.site.register(OrderItem)
