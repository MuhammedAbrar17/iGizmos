from django.shortcuts import render,redirect,get_object_or_404
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



def remove_coupon(request, coupon_id):
    if request.method == "POST":
        coupon = get_object_or_404(Coupon, id=coupon_id)
        coupon_name = coupon.coupon_code
        coupon.delete()
        messages.success(request, f'Coupon "{coupon_name}" removed successfully')
        return redirect('addcoupon')

    # Handle GET request if needed (e.g., showing a confirmation page)
    coupon = get_object_or_404(Coupon, id=coupon_id)
    context = {
        'coupon': coupon,
    }
    return render(request, "adminpanel/remove_coupon.html", context)

