
from django.urls import path
from authapp import views

urlpatterns = [
    path('login',views.handle_login,name='handle_login'),
    path('signup',views.signup,name='signup'),
    path('forgotpass',views.forgotpass,name='forgotpass'),
    path('logout',views.handle_logout,name='handle_logout')
     
] 