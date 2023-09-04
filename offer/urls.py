from .import views
from django.urls import path 

urlpatterns = [
   path('addcoupon/',views.add_coupon, name='addcoupon'),
   path('remove_coupon/<int:coupon_id>/', views.remove_coupon, name='remove_coupon'),
   
]