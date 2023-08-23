from .import views
from django.urls import path 

urlpatterns = [
   path('addcoupon/',views.add_coupon, name='addcoupon'),
   
]