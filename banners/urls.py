from django.urls import path,include
from . import views


urlpatterns = [
   
    path('addbanner/',views.add_banner,name='addbanner'),
    path('removebanner/<int:banner_id>/',views.remove_banner,name='removebanner'),
    path('middlebannet',views.add_midle_banner,name='middlebanner'),
    path('removemiddlebaner/<int:middlebaner_id>/',views.remove_middle_banner,name='removemiddlebanner'),
]