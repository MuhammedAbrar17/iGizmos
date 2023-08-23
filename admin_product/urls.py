
from django.urls import path,include
from . import views


urlpatterns = [
    path('products/',views.products, name='products'),
    path('addproducts/',views.add_product,name='addproduct'),
    path('product/deleteproduct/<int:id>/',views.delete_product, name='deleteproduct'),
    path('product/editproduct/<int:id>/',views.edit_product, name='editproduct'),
    path('addcategory/',views.add_category, name='add_category'),
    path('editcategory/<int:id>/',views.edit_category, name='editcategory'),
    path('deletecategory/<int:id>/',views.delete_category, name='deletecategory'),
    path('addbrand/',views.add_brand, name='addbrand'),
    path('editbrand/<int:id>/',views.edit_brand, name='editbrand'),
    path('variant',views.variant,name='variant'),
    path('addvariant/<int:id>',views.addvariant,name='addvariant')
    # path('deletebrand/<int:id>/',views.delete_brand, name='delete_brand'),
]
    