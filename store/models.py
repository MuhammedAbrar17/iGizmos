from django.db import models
from category.models import AdminCategory,Brand
from django import forms
from offer.models import Offer


# Create your models here.
class product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug =  models.SlugField(max_length=200,unique=True,blank=True)
    product_desc = models.TextField(max_length=100,blank=True)
    image = models.ImageField(upload_to='photos/products')
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(AdminCategory,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=None)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now_add=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.product_name
    
    def is_outofstock(self):
        return self.stock <=0
    
    def get_variant(self,ram=None):
        return ProductVariant.objects.get(product=self.id,ram=ram)
    
    def get_offer_price(self,variant):
        p_price = 0
        if self.offer:
            p_price = variant.price * (self.offer.off_percent/100)
            
        else:
            p_price = 0
            
          
        return p_price
    
    
    
    
class ProductVariant(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE , related_name='productVariant')
    quantity = models.IntegerField(default=0)
    price = models.IntegerField()
    ram = models.CharField(max_length=10)
    storage = models.CharField(max_length=10)
    
    def get_offer_price(self):
        return round((self.price - (self.product.offer.off_percent / 100) * self.price))
   
    
    

    
class Productimage(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE,related_name="product_images")
    pr_images = models.ImageField(upload_to="photos/product")
    
    def __str__(self):
        return self.product.product_name +'image'
  
  
    

    
       
    
    

    
    
    
 
    
        


   