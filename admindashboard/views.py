# admindashboard/views.py

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from authapp.views import handle_login
from order.models import *
from store.models import *
from category.models import *
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from django.db.models import F
import calendar


def admin_dashboard(request):
    if request.user.is_authenticated and  request.user.is_superuser:
        return render(request, "adminpanel/adminindex.html")
    if not request.user.is_superuser:
        return redirect(handle_login)


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

#sales report

@login_required(login_url='handle_login')
def sales_report(request):
    if not request.user.is_superuser:
        return redirect(handle_login)
    
    context = {}

    if request.method == 'POST':

        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')

        if start_date == '' or end_date == '':
            messages.error(request,'Give date first')
            return redirect(sales_report)
        
        if start_date ==  end_date :
            date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            order_items = OrderItem.objects.filter(order__created_at__date=date_obj.date())
            if order_items:
                context.update(sales = order_items,s_date=start_date,e_date = end_date)
                return render(request,'adminpanel/sales.html',context)
            else:
                messages.error(request,'no data found')
            return redirect(sales_report)

        order_items = OrderItem.objects.filter(order__created_at__gte=start_date, order__created_at__lte=end_date)

        if order_items:
            context.update(sales = order_items,s_date=start_date,e_date = end_date)
        else:
            messages.error(request,'no data found')

    return render(request,'adminpanel/sales.html',context)
