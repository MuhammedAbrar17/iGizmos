from django.db import models
from store.models import product,ProductVariant
from django.contrib.auth.models import User
from offer.models import Coupon


# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    def __str__(self):
        return self.cart_id
    
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE,null=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.variant.price * self.quantity
    
    def sub_total_with_offer(self):
        return int((self.sub_total()) - ( self.sub_total() * self.product.offer.off_percent / 100))
    
    
    
    def __str__(self):
        return self.product.product_name
        
    