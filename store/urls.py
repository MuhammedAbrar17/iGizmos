from django.urls import path
from .import views

urlpatterns = [
    
    path('',views.store,name='store'),
    path('produuct/<slug:product_slug>/', views.product_details, name='product_details'),
    path('search/', views.search_products, name='search_products'),
   
]
