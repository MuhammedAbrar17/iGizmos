from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import *
from authapp.views import *
from django.contrib.auth.decorators import login_required


@login_required(login_url='handle_login')
def add_banner(request):
    if not request.user.is_superuser:
        return redirect(handle_login)
    if request.method=="POST":
        image = ""
        try:
            image = request.FILES['image']
            
        except:
            
            if image == "":
                messages.info(request,"Image field can't be empty")
                return redirect(add_banner)
            
        title = request.POST['title']
        content=request.POST['content']
        startdate=request.POST['startdate']
        enddate = request.POST['enddate'] 
        
        if startdate == "" and enddate=="":
            messages.error(request,"Give date first")
            return redirect(add_banner)
        banner = Banner.objects.create(
            title = title,
            image = image,
            content = content,
            start_date = startdate,
            end_date = enddate,
        )
        banner.save()
        
        messages.info(request,'banner create succefuly')
        return redirect(add_banner)
    
    banners  =Banner.objects.all()
    
    context={
        'banner':banners
    }
            
    return render(request,'adminpanel/add_banner.html',context)
        
        
def remove_banner(request,banner_id):
    
        banner = get_object_or_404(Banner,id = banner_id)
        banner_title = banner.title
        banner.delete()
        messages.success(request,f'banner "{banner_title}"removed successfuly')
        return redirect(add_banner)
            
            
@login_required(login_url='handle_login')
def add_midle_banner(request):
    if not request.user.is_superuser:
        return redirect(handle_login)
    if request.method=="POST":
        image = ""
        try:
            image = request.FILES['image']
            
        except:
             
            if image == "":
                messages.info(request,"Image field can't be empty")
                return redirect(add_banner)
        title = request.POST['title']
        content = request.POST['content']
        
        
        midlebanner = MiddleBanner.objects.create(
            title = title,
            content = content,
            image = image,
            
        )  
        midlebanner.save()
        
        messages.info(request,'midle_banner create succefuly')
        return redirect(add_midle_banner)
    midlebanner = MiddleBanner.objects.all()
    context = {
        'middlebaner':midlebanner
    }
     
    return render(request,'adminpanel/midlebanner.html',context)
               
               
            
            
def remove_middle_banner(request,middlebaner_id):
    
        middlebaner = get_object_or_404(MiddleBanner,id = middlebaner_id)
        banner_title = middlebaner.title
        middlebaner.delete()
        messages.success(request,f'banner "{banner_title}"removed successfuly')
        return redirect(add_midle_banner)    
    
    