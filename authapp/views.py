from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
import random
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.cache import cache_control


# Create your views here.

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def handle_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')  
        user = authenticate(request,username=username,password=password)
        if user is not None:
         
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid username or password")
            return redirect(handle_login)
        
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def signup(request):
    if request.method=='POST':
        get_otp = request.POST.get('otp')
        if not get_otp:
            username = request.POST.get('Username')
            fname= request.POST.get('Firstname')
            lname=request.POST.get('Lastname')
            email=request.POST.get('email')
            pass1=request.POST.get('pass1')
            pass2=request.POST.get('pass2')
            
            if not username.strip():
                messages.error(request,"Username is required")
                return redirect('signup')
            if not fname.strip():
                messages.error(request,"First name is required")
                return redirect('signup')
            if not lname.strip():
                messages.error(request,"Last name is required")   
                return redirect('signup')
            if not email.strip():
                messages.error(request,"Email is mrequired")
                return redirect('signup')
            if pass1 != pass2:
                messages.error(request,"password do not match")
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.error(request,'This email address is alredy taken')
                return redirect('signup')
           
            myuser = User.objects.create_user(username=username,email=email,password=pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = False
            myuser.save()
            otp = int(random.randint(1000,9999))
            prof = Profile(user = myuser,otp =otp)
            prof.save()
            mesg = f'Hello\t{myuser.username},\nYour OTP to verify your account for iGizmos is {otp}\nThanks!'
            send_mail(
            "Welcome to iGizmos Verify Your Emalil",
            mesg,
            settings.EMAIL_HOST_USER,
            [myuser.email],
            fail_silently=False
            )
            return render(request,'signup.html',{'otp':True,'usr':myuser})
        else:
            get_email = request.POST.get('email')
            user = User.objects.get(email = get_email)
            if get_otp == Profile.objects.filter(user=user).last().otp:
                user.is_active = True
                user.save()
                messages.success(request,f'Account is created for {user.email}')
                Profile.objects.filter(user=user).delete()
                return redirect(handle_login)
            else:
               messages.warning(request,f'You Entered a wrong OTP')
               return render(request,'signup.html',{'otp':True,'usr':user})       
    
    if request.user.is_authenticated:
        return redirect('/')
    return render(request,'signup.html',{'otp':False})
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def handle_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def otp_login(request):
    
    if request.method=="POST":
        get_otp = request.POST.get('otp')
        if not get_otp:
            email = request.POST.get('email')
            try:
                user = User.objects.get(email = email)
            except:
                messages.error(request,f"This is not a valid email id")
                return redirect(otp_login)


            if user is not None:
                otp = int(random.randint(1000,9999))
                profile = Profile(user = user, otp = otp)
                profile.save()
                mess=f'Hello\t{user.username},\nYour OTP to Login your account for iGizmos is {otp}\nThanks!'
                send_mail(
                "welcome to iGizmos Verify your Email for login",
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
                )   
                return render(request,'otp_login.html',{'otp':True,'usr':user})
        else:            
            get_email = request.POST.get('email')
            user = User.objects.get(email = get_email)
            if get_otp == Profile.objects.filter(user=user).last().otp:
                login(request, user)
                messages.success(request,f'Successfully logined {user.email}')
                Profile.objects.filter(user=user).delete()
                return redirect('/')
            else:
               messages.warning(request,f'You Entered a wrong OTP')
               return render(request,'otp_login.html',{'otp':True,'usr':user})
    if request.user.is_authenticated:
        return redirect('/')
    
    return render(request, 'otp_login.html')   



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def forgot_password(request):
    if request.method=="POST":
        get_otp = request.POST.get('otp')
        if not get_otp:
            email = request.POST.get('email')
            try:
                user = User.objects.get(email = email)
            except:
                messages.error(request,f"This is not a valid email id")
                return redirect(forgot_password)


            if user is not None:
                otp = int(random.randint(1000,9999))
                profile = Profile(user = user, otp = otp)
                profile.save()
                mess=f'Hello\t{user.username},\nYour OTP to resetting password for iGizmos account - {otp}\nThanks!'
                send_mail(
                "welcome to iGizmos Verify your Email for password resetting",
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
                )   
                return render(request,'forgotpassword.html',{'otp':True,'usr':user})
        else:            
            get_email = request.POST.get('email')
            user = User.objects.get(email = get_email)
            if get_otp == Profile.objects.filter(user=user).last().otp:
                Profile.objects.filter(user=user).delete()
                return render(request, 'resetpassword.html',{'usr':user})
            else:
               messages.warning(request,f'You Entered a wrong OTP')
               return render(request,'otp_login.html',{'otp':True,'usr':user})
            
    if request.user.is_authenticated:
        return redirect('/')

    return render(request, 'forgotpassword.html')
 
@login_required(login_url='handle_login')
def reset_password(request):
    if  request.method == "POST":
        pass1 = request.POST['password']
        pass2 = request.POST["pass1"]

        get_email = request.POST.get('email')
        user = User.objects.get(email = get_email) 
        if pass1 == pass2:
            user.set_password(pass1)
            user.save()
            messages.success(request, 'Password succesfully changed')
            return redirect('handle_login')
        else:
            messages.error(request, 'passwords not matching')
            return redirect(reset_password)
        
