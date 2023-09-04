from django.db import models
from django.contrib.auth.models import User
from user_profile.models import UserAddress
from store.models import product
import string
import random
from datetime import datetime
from store.models import ProductVariant


# Create your models here.
def generate_order_id():
    """Generate a 14-cahracter order ID"""
    while True:
        letters = string.ascii_uppercase + string.digits
        order_id = ''.join(random.choice(letters) for i in range(9))
        year = str(datetime.now().year)[-2:]
        month=str(datetime.now().month)[-2:]
        day = str(datetime.now().day)
        hour = str(datetime.now().hour)
        new_id = 'iGiz' + year + month + day + hour+ order_id
        return new_id
    
class PaymentMethod(models.Model):
    method = models.CharField(max_length=50)
    
    
class Payment(models.Model):
    STATUS=[
        
        ('pending', 'Pending'),
        ('done', 'Done'),
    ]   
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod,on_delete=models.CASCADE)
    amount_paid = models.FloatField(null=True)
    status = models.CharField(max_length=20, choices=STATUS,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.payment_method.method
    
class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True, blank=True)
    order_id = models.CharField(max_length=50, default=generate_order_id, unique=True)
    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL,null=True, blank=True)
    order_total = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    coupon_discount = models.BigIntegerField(null=True,blank=True)
    coupon = models.ForeignKey('offer.Coupon', on_delete=models.SET_NULL,null=True, blank=True)
    
        
    def __str__(self):
        return self.order_id
    
class OrderItem(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(product, on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True, blank=True)
    product_price = models.FloatField()
    quantity = models.IntegerField()
    total = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    product_variant = models.ForeignKey(ProductVariant,on_delete=models.SET_NULL,null=True)

    def sub_total(self):
        return self.product_price * self.quantity
    
    def __unicode__(self):
        return self.product
    
    
    