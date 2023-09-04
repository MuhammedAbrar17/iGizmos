from django.shortcuts import render,redirect,get_object_or_404
from .models import Cart,CartItem
from store.models import product,ProductVariant
from django.http import HttpResponse
from offer.models import Coupon
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
    
def add_cart(request,product_id,variant_id):  
    variant = ProductVariant.objects.get(id = variant_id)
    products = product.objects.get(id=product_id) #get the product
    try:
        print(_cart_id(request))
        cart = Cart.objects.get(cart_id=_cart_id(request))#get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.coupon = None    
    cart.save()
    
    try:
        cart_item = CartItem.objects.get(product = products,cart = cart ,variant = variant)
        # if ((variant.quantity)-(cart_item.quantity + 1)) < 0:
        #     messages.warning(request,"Out of Stock")
        #     return redirect('cart') 
        cart_item.quantity += 1 #cart_item.quantity = cart_item.quantity +1
        cart_item.save()
    except CartItem.DoesNotExist:
        user_instance = request.user if request.user.is_authenticated else None  # For guest users
        cart_item = CartItem.objects.create(
            variant = variant,
            product = products,
            quantity = 1,
            cart = cart,
            user = user_instance,
        )
        cart_item.save()
      
    return redirect('cart')
        
        
def remove_cart(request,product_id,variant_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    products = get_object_or_404(product,id=product_id)
    variant = ProductVariant.objects.get(id = variant_id)
    cart_item = CartItem.objects.get(product=products,cart=cart, variant = variant)
    cart.coupon = None
    cart.save()
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()    
        
    return redirect('cart')    

def remove_cart_item(request,product_id,variant_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    products = get_object_or_404(product, id=product_id)
    variant = ProductVariant.objects.get(id = variant_id)
    cart_item = CartItem.objects.get(product=products,cart=cart,variant = variant)
    cart_item.delete()
    cart.coupon = None
    cart.save()
    return redirect('cart')
    

def cart(request, total=0, quantity=0, cart_item=None,coupons = None):

    discount_amount = 0 
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    coupons = Coupon.objects.all()
    grand_total = 0
    for cart_item in cart_items:
        total += (cart_item.variant.price * cart_item.quantity)
        quantity += cart_item.quantity
        grand_total = total
        print("********************************varients :::::", cart_item.variant.ram)
        
        
    if request.method == "POST":
        coup = request.POST['search']
        print(coup)
        try:
            
            coupon = Coupon.objects.get(coupon_code = coup)
            if coupon.is_expired():
                messages.error(request, 'Coupon is expired')
                return redirect('cart')
            
            
            if coupon.min_amount > total:
                messages.error(request, f'Amount should be greater than {coupon.min_amount}')
                return redirect('cart')
            
            cart = Cart.objects.get(cart_id = _cart_id(request))
            
            discount_amount = total * coupon.off_percent / 100

            if discount_amount > coupon.max_discount:
                discount_amount = coupon.max_discount

            subtotal = total    
            grand_total -= discount_amount

            cart.coupon = coupon
            cart.save()
            
        except:
            print('out of try')
            messages.error(request, 'Coupon not found')
            return redirect('cart')    
            

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total':grand_total,
        'coupons': coupons,
        'cart':cart,
        'discount_amount':discount_amount,
        
    }

    return render(request, 'cart.html', context)
