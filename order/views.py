from django.http import HttpResponse
from django.shortcuts import redirect, render
from user_profile.models import UserAddress, WalletTransaction, Wallet
from cart.models import *
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from cart.views import _cart_id
from django.contrib.auth.decorators import login_required
import razorpay
from decimal import Decimal
from django.contrib import messages
from checkout.views import checkout


# Create your views here.
@login_required(login_url='handle_login')
def payments(request, total = 0, pretotal=0):

    # saving payment details
    if request.user.is_authenticated:
        current_user = request.user
        payment_method = PaymentMethod.objects.get(id=1)
        payment = Payment(
            user = request.user,
            payment_method = payment_method,
        )
        payment.save()
        if request.method == "POST":
            addr = request.POST['address']
            address = UserAddress.objects.get(id=addr)
        else:
            address = UserAddress.objects.filter(user=current_user).order_by('-id').first() 

        order = Order.objects.filter(user=request.user).order_by('-id').first()
        order.payment = payment
        order.status = 'accepted'
        order.save()

        # move cart items to ordered items
        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            
            product_price = 0
            if cart_item.product.offer:
                product_price = cart_item.variant.get_offer_price()
            else:
                product_price = cart_item.variant.price
            product_variation = cart_item.variant
                

            orderitem = OrderItem(
                user = request.user,
                order = order,
                product = cart_item.product,
                product_variant = product_variation,
                payment = payment,
                product_price = product_price,
                quantity = cart_item.quantity,
                total = product_price * cart_item.quantity,
                status = 'accepted',
            )
            orderitem.save()

            total += orderitem.sub_total()


    
        # Reduce stock of ordered product
            variant = ProductVariant.objects.get(id=cart_item.variant_id)
            products = product.objects.get(id=cart_item.product.id)
            variant.quantity -= cart_item.quantity
            variant.save()
        
        # order message
        mess=f'Hello\t{request.user.username},\nYour Order of { order.order_id } has confirmed.\nThanks!'
        send_mail(
        "Thank you for the order",
        mess,
        settings.EMAIL_HOST_USER,
        [request.user.email],
        fail_silently=False
        )
        # Removing Cart items
        CartItem.objects.filter(user=request.user).delete()
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart.coupon = None
        cart.save()

        orderitems = OrderItem.objects.filter(user=request.user, order=order)
        if order.coupon_discount:
            pretotal=total
            total -= order.coupon_discount
            

        context = {
            'order' : order,
            'orderitems' : orderitems,
            'total' : total,
            'pretotal':pretotal,
            
        }
        return render(request, "invoice.html", context)


@login_required(login_url='handle_login')
def place_order(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        total = 0
        discount_amount = None
        cart_items = CartItem.objects.filter(user=current_user)
        print(cart_items)
        cart_count = cart_items.count()
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.variant.quantity :
                print("cart item out of stock")
                return redirect('cart')
            if cart_item.product.offer:
                total += cart_item.sub_total_with_offer()
            
            else:
                total += (cart_item.variant.price * cart_item.quantity)
            cart = Cart.objects.get(cart_id=_cart_id(request))
            if cart.coupon:
                
                discount_amount = total * cart.coupon.off_percent / 100
                

                if discount_amount > cart.coupon.max_discount:
                    discount_amount = cart.coupon.max_discount

                
                total -= discount_amount
                
        
        if cart_count <= 0:
            return redirect('store')

        if request.method == "POST":
            addr = request.POST['address']
            
            address = UserAddress.objects.get(id=addr)
            
        else:
            address = UserAddress.objects.filter(user=current_user).order_by('-id').first() 

        data = Order()
        data.user = current_user
        data.address = address
        data.order_total = total
        data.coupon_discount = discount_amount
        if cart.coupon:
            data.coupon = cart.coupon
    
        data.save()
        order = Order.objects.get(user = current_user, status=data.status, order_id=data.order_id)
        
        client = razorpay.Client(auth= ( settings.KEY, settings.KEY_SECRET ))
        payment = client.order.create({'amount' :total * 100 , 'currency' :'INR', 'payment_capture' : 1 })
        
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        print('---------wallet ------------------>>',wallet)

        
        
        
        

        context = {
            'order' : order,
            'cart_items' : cart_items,
            'total' : total,
            'payment' : payment,
            'discount_amount': discount_amount, 
            'wallet' : wallet
            
        }
        return render(request,'payment.html', context)

@login_required(login_url='handle_login')    
def my_orders(request):
    
    myorders = OrderItem.objects.filter(Q(user=request.user) & ~Q(status='pending')).order_by('-created_at')
    context = {
        "myorders":myorders,
    }
    return render(request, 'myorders.html', context)


@login_required(login_url='handle_login')
def cancel_orders(request, id):
     
    item = OrderItem.objects.get(id = id)
    
    if(item.order.payment.payment_method.method != 'Cash on Delivery' and item.order.coupon_discount):
        item.status = 'cancelled'
        quantity = item.quantity
        item.product_variant.quantity += quantity
        item.save()

        OrderItems = OrderItem.objects.filter(order=item.order)
        minPurchaseAmount =  item.order.coupon.min_amount
        total = 0
        for order_item in OrderItems:
            if order_item.status != 'cancelled':
                total+=order_item.sub_total()
        
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        cancelled_amount = item.sub_total()

        if(minPurchaseAmount>total):
            
            discount_price = item.order.coupon_discount
            print('discount price --> ',discount_price)
            if(discount_price>cancelled_amount):
                discount_percentage = (cancelled_amount/ total)
                print('discount_percentage ---> ',discount_percentage)
                deducting_amount = discount_percentage * discount_price
                print('deducting amount (from if) --> ',deducting_amount)
            else:
                deducting_amount = discount_price
                print('deducting amount (from else)--> ',deducting_amount)
            amount = cancelled_amount - deducting_amount
            wallet.balance += Decimal(amount)
            wallet.save()
            description = f'Cancel Order -> {cancelled_amount} - {deducting_amount}'
            wallet_transaction = WalletTransaction.objects.create(
                wallet=wallet, description=description, 
                type='Credit', 
                amount=round(amount)
            )
        else:
            print('===========================')
            amount = Decimal(cancelled_amount)
            wallet.balance += amount
            wallet.save()
            description = 'Cancelled order'
            wallet_transaction = WalletTransaction.objects.create(
                wallet=wallet, description=description, 
                type='Credit', 
                amount=round(amount)
            )
            messages.success(request, 'Amount credited in your wallet')       
    elif item.order.payment.payment_method.method != 'Cash on Delivery' :
        quantity = item.quantity
        item.product_variant.quantity += quantity
        item.status = 'cancelled'
        item.save()

        amount = Decimal(item.product_price)
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        wallet.balance += amount
        wallet.save()
        description = 'Cancelled order'
        wallet_transaction = WalletTransaction.objects.create(
            wallet=wallet, description=description, 
            type='Credit', 
            amount=round(amount)
        )
        messages.success(request, 'Amount credited in your wallet') 
    else:
        item.status = 'cancelled'
        quantity = item.quantity
        item.product_variant.quantity += quantity
        item.save()

        current_user = request.user
        subject = "Cancell order succesfull!"
        mess = f'Greetings {current_user.first_name}.\nYour Order {item.order.order_id} has been cancelled. \nThank you for shopping with us!'
        send_mail(
                subject,
                mess,
                settings.EMAIL_HOST_USER,
                [current_user.email],
                fail_silently = False
        )
    return redirect(my_orders)
        
    
    
   

@csrf_exempt
def pre_success(request):
    return redirect(success)


# for order confirmation page and adding payment details
@login_required(login_url='handle_login')
def success(request, total = 0,pretotal = 0):
        
        payment_method = PaymentMethod.objects.get(id=2)
        payment = Payment(
            user = request.user,
            payment_method = payment_method,
            status = 'Paid'
        )
        payment.save()
        order = Order.objects.filter(user=request.user).order_by('-id').first()
        order.payment = payment
        order.status = 'accepted'
        order.save()
        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            product_price = 0
            if cart_item.product.offer:
               product_price = cart_item.variant.get_offer_price()
            
            else:
                product_price = cart_item.variant.price
            product_variation = cart_item.variant
            orderitem = OrderItem(
                user = request.user,
                order = order,
                product = cart_item.product,
                product_variant = product_variation,
                payment = payment,
                product_price = product_price,
                total = product_price * cart_item.quantity,
                quantity = cart_item.quantity,
                
                status = 'accepted',
            )
            orderitem.save()

            total += orderitem.sub_total()
            
            
        # Reduce stock of ordered product
            variant = ProductVariant.objects.get(id=cart_item.variant_id)
            products = product.objects.get(id=cart_item.product.id)
            variant.quantity -= cart_item.quantity
            variant.save()
        
        # order message
        mess=f'Hello\t{request.user.username},\nYour Order of { order.order_id } has confirmed.\nThanks!'
        send_mail(
        "Thank you for the order",
        mess,
        settings.EMAIL_HOST_USER,
        [request.user.email],
        fail_silently=False
        )
        # Removing Cart items
        CartItem.objects.filter(user=request.user).delete()
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart.coupon = None
        cart.save()

        orderitems = OrderItem.objects.filter(user=request.user, order=order)
        if order.coupon_discount:
            pretotal=total
            total -= order.coupon_discount
        context = {
            'order' : order,
            'orderitems' : orderitems,
            'total' : total,
            'pretotal':pretotal,
            
        }
        return render(request, "invoice.html", context)


# invoice function
@login_required(login_url='handle_login')
def invoice(request, id):
    total = 0
    pretotal = 0
    # id from user side(my orders)
    order_item = OrderItem.objects.get(id = id)
    # for retreving the order
    order = Order.objects.get(order_id = order_item.order.order_id)
    # for retreving all ordered items in that order
    order_items = OrderItem.objects.filter(order = order)
    for item in order_items:
        total += item.sub_total()
        if order.coupon_discount:
            pretotal = total
            total -= order.coupon_discount
    
    context = {
        'order':order,
        'orderitems':order_items,
        'total' : total,
        'pretotal':pretotal,
        'f':True,

    }
    return render(request, 'invoice.html', context)



def wallet(request):
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    transactions = WalletTransaction.objects.filter(wallet=wallet)
    context = {'wallet': wallet}
    if transactions.exists():
        context['transactions'] = transactions

    return render(request, "wallet.html", context)

@login_required(login_url='handl_elogin')
def walletpayments(request, total=0, pretotal=0):
    if request.user.is_authenticated:
        user = request.user
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        print('wallet >> ::---------------',wallet)
        # Check if the user has enough balance in their wallet
        if wallet.balance >= total:
            # Deduct the payment from the user's wallet balance
            

            # Create a payment record for wallet payment
            payment_method = PaymentMethod.objects.get(id=3)  # Assuming PaymentMethod ID for Wallet Payment
            payment = Payment(
                user=user,
                payment_method=payment_method,
            )
            payment.save()

            # Update the order status and associate it with the payment
            order = Order.objects.filter(user=user).order_by('-id').first()
            order.payment = payment
            order.status = 'accepted'
            order.save()

            # Move cart items to ordered items
            cart_items = CartItem.objects.filter(user=user)
            for cart_item in cart_items:
                product_price = 0
                
                if cart_item.product.offer:
                    product_price = cart_item.variant.get_offer_price() 
               
                else:
                    product_price = cart_item.variant.price
                product_variation = cart_item.variant

                # Create an order item for each cart item
                order_item = OrderItem(
                    user=user,
                    order=order,
                    product=cart_item.product,
                    product_variant = product_variation,
                    payment=payment,
                    product_price=product_price,  # Assuming no offer for simplicity
                    quantity=cart_item.quantity,
                    total = product_price * cart_item.quantity,
                    status='accepted',
                )
                order_item.save()

                total += order_item.sub_total()


                # Reduce the product's stock
                variant = ProductVariant.objects.get(id=cart_item.variant_id)
                products = product.objects.get(id=cart_item.product.id)
                variant.quantity -= cart_item.quantity
                variant.save()
                
                

            # Clear the user's cart
            CartItem.objects.filter(user=user).delete()
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart.coupon = None
            cart.save()

            # Calculate order total and discounts
            orderitems = OrderItem.objects.filter(user=user, order=order)
            if order.coupon_discount:
                pretotal = total
                total -= order.coupon_discount
            
            wallet.balance -= total
            wallet.save()
            description = 'Product purchased'
            wallet_transaction = WalletTransaction.objects.create(
            wallet=wallet, description=description, type='Debit', amount=total)
            messages.success(request, 'Amount Debited in your wallet')

            context = {
                'order': order,
                'orderitems': orderitems,
                'total': total,
                'pretotal': pretotal,
                
            }

            return render(request, "invoice.html", context)
       

    return render(request, 'payment.html')