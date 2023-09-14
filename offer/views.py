from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Coupon,Offer
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


@login_required(login_url='handle_login')
def add_offer(request):
    if request.method == "POST":
        name = request.POST['name']
        percentage = request.POST['perc']
        start_date = request.POST['start-date']
        end_date = request.POST['end-date']

        if start_date == '' or end_date == '':
            messages.error(request,'Give date first')
            return redirect(add_offer)

        offer = Offer.objects.create(
            name = name,
            off_percent = percentage,
            start_date = start_date,
            end_date = end_date,
        )
        offer.save()
        messages.success(request,f'Offer "{name}" created')
        return redirect(add_offer)
    offer = Offer.objects.all()
    context = {
        'offers' : offer,
    }
    return render(request, "adminpanel/offer.html", context)

