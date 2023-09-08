
from django.urls import path
from authapp import views

urlpatterns = [
    path('login',views.handle_login,name='handle_login'),
    path('signup',views.signup,name='signup'),
    path('logout',views.handle_logout,name='handle_logout'),
    path('forgotpassword',views.forgot_password,name='forgotpassword'),
    path('otp_login/',views.otp_login, name='otp_login'),
    path('resetpassword/',views.reset_password, name='resetpassword'), 
] 