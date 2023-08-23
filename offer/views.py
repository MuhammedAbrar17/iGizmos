from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Coupon
from django.contrib import messages


# Create your views here.
#for adding new coupons----------------------------------------------
@login_required(login_url='admin_login')
def add_coupon(request):
    if request.method == "POST":
        name = request.POST['name']
        percentage = request.POST['perc']
        min_amount = request.POST['min']
        max_discount = request.POST['max']
        end_date = request.POST['end-date']

        coupon = Coupon.objects.create(
            coupon_code = name,
            off_percent = percentage,
            min_amount = min_amount,
            max_discount = max_discount,
            expiry_date = end_date,
        )
        coupon.save()
        messages.success(request,f'Coupon "{name}" created')
        return redirect(add_coupon)
    coupon = Coupon.objects.all()
    context = {
        'coupons' : coupon,
    }
    return render(request, "adminpanel/coupon.html", context)
