from django.db import models



class AdminCategory(models.Model):  # Rename 'category' to 'AdminCategory'
    category_decs = models.TextField(max_length=100, blank=True, null=True)
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    cat_img = models.ImageField(upload_to='photos/categories', blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name

    
 
class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)
    brand_desc = models.TextField(max_length=500, blank=True)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return self.brand_name   
    
        