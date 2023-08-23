from django.shortcuts import render,redirect
from .models import Wishlist
from store.models import product
from django.contrib import messages


# Create your views here.
def wishlist(request):
    usr = request.user.id
    try:
        products = Wishlist.objects.filter(user = usr)
    except:
        products = ''
    return render(request,'wishlist.html',{'wishlisted':products})

def add_wishlist(request,id):
    user = request.user
    try:
        wishlist = Wishlist.objects.get(user=user,product=id)
    except Wishlist.DoesNotExist:
        products = product.objects.get(id=id)
        whislist = Wishlist(user = user, product = products)
        whislist.save()
    messages.success(request,'Item added to wishlist')
    try:
        products = product.objects.get(id=id)
    except Exception as e:
        raise e
    return redirect('product_details',products.slug)
        
        
        
        