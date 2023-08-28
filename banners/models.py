from django.db import models

# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='banners/')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.title
    


class MiddleBanner(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='middle_banners/')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    