# admindashboard/views.py

from django.shortcuts import render,redirect
from django.contrib.auth.models import User

def admin_dashboard(request):
    if request.user.is_authenticated and  request.user.is_superuser:
        
        return render(request, "adminpanel/adminindex.html")


#user details-----------
def user_details(request):
    if not request.user.is_authenticated and not request.user.is_superuser:
        return redirect('home')
    usr = User.objects.all()  
    context = {

        'users' : usr
    }
    return render(request, 'adminpanel/user.html', context)



def user_action(request, id):
    if not request.user.is_authenticated and not request.user.is_superuser:
        return redirect('home')
    usr = User.objects.get(id=id)
    if usr.is_active:
        usr.is_active = False
        usr.save()
        return redirect(user_details)
    else:
        User.objects.get(id=id)
        usr.is_active = True
        usr.save()  
        return redirect(user_details)


def search_users(request):  
    if not request.user.is_authenticated and not request.user.is_superuser:
        return redirect('home')
    search_text = request.POST['query']
    context = {
        'users': User.objects.filter(username__icontains=search_text),
        'search_text':search_text,
    }
    return render(request,'adminpanel/user.html',context)
