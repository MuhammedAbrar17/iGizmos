from django.shortcuts import render
from store.models import product
from banners.models import Banner,MiddleBanner
# Create your views here.
def home(request):
    products = product.objects.filter(is_available = True)
    active_middle_banner = MiddleBanner.objects.filter(is_active=True).first()
    active_banners = Banner.objects.filter(is_active=True)
   
    
    context = {
        'products': products,
        'active_banners':active_banners,
        'active_middle_banner': active_middle_banner,
        
    }
    return render(request,"index.html", context)


