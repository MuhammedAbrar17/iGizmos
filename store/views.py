from django.shortcuts import render,get_object_or_404
from store.models import product,ProductVariant
from wishlist.models import Wishlist
from category.models import AdminCategory,Brand
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.
# def store(request,category_slug=None):
#     categories = None
#     products = None
    
#     if category_slug != None:
#         categories = get_object_or_404(AdminCategory,slug=category_slug)
#         products = product.objects.filter(category=categories,is_available=True)
#     else:   
#         products = product.objects.all()
#         print(products)
#     context = {
#         'products': products,
        
        
#     }
#     return render(request,'shop.html',context)

def store(request):
    products = product.objects.all().filter(is_available = True )
    categories = AdminCategory.objects.all()
    brand = Brand.objects.all()
    paginator = Paginator(products,6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    
    context = {
        'products' :  paged_products ,
        'categories' : categories,
        'brands' : brand,
        
        
    }
   
    return render(request, 'shop.html', context)



def product_details(request, product_slug):
    is_wish=None
    try:
        single_product = product.objects.get(slug = product_slug)
        
    except Exception as e:
        raise e
    
    try:
        if request.user.is_authenticated:
            is_wish = Wishlist.objects.get(user=request.user, product = single_product)
            
    except:
        pass
    
            
    context = {
        'single_product' : single_product,
        'selected_ram':single_product.productVariant.first().ram,
        'selected_variant':single_product.productVariant.first(),
        'is_wish' : is_wish,
    }
    if request.GET.get('ram'):

            ram = request.GET.get('ram')
            variant = single_product.get_variant(ram=ram)
            context['selected_ram'] = ram
            context['selected_variant'] = variant
            
    return render(request, 'single.html', context)


#search prodect------


def search_products(request):
    search_query = request.GET.get('q', '')

    filtered_products = product.objects.filter(is_available=True)
    c = 0
    count = 0
    if search_query:
        count += 1
        filtered_products = filtered_products.filter(
            Q(product_name__icontains=search_query) |
            Q(product_desc__icontains=search_query)
        )
        c = filtered_products.count()
   

    context = {
        'products': filtered_products,
        'c': c,
        'f': True,
    }

    return render(request, 'shop.html', context)

def filtered_products(request):
    # Retrieve the filter options selected by the user from the URL query parameters
    selected_categories = request.GET.getlist('category')
    selected_brands = request.GET.getlist('brand')
    min_price = request.GET.get('min_price')  # Get minimum price from query params
    max_price = request.GET.get('max_price')  # Get maximum price from query params


    # Query the database to get the filtered products
    # filteredproduct = ProductVariant.objects.all().filter(is_avilable = True)
    filtered_products = product.objects.all().filter(is_available = True)
    count = 0
    c = 0
    
    if selected_categories:
        filtered_products = filtered_products.filter(category__in=selected_categories)
        c = filtered_products.count()
        count += 1

    if selected_brands:
        filtered_products = filtered_products.filter(brand__in=selected_brands)
        count += 1
        c = filtered_products.count()
    
    if count == 0:
        filtered_products = None
        
        
    # if min_price and max_price:
    #     filteredproduct = filteredproduct.filter(price__gte=min_price, price__lte=max_price)
    #     count += 1
    #     c = filteredproduct.count()    

    


    categories = AdminCategory.objects.all()
    brand = Brand.objects.all()

    context = {
        'products' : filtered_products,
        
        'categories' : categories,
        'brands' : brand,
        'c' : c,
        'f': True,
    }

    return render(request, 'shop.html', context)

