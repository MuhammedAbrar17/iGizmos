
from os import name
from django.shortcuts import redirect, render
from store.models import product,Productimage,ProductVariant
from django.contrib import messages
from category.models import Brand
from category.models import AdminCategory  
from django.contrib.auth.decorators import login_required
from authapp.views import *
from authapp import *
# Create your views here.

# Product section
@login_required(login_url='handle_login')
def products(request):
    if not request.user.is_superuser:
        return redirect(handle_login)
    products = product.objects.all().filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request,'adminpanel/page-products-grid-2.html',context)
@login_required(login_url='handle_login')
def add_product(request):
    if not request.user.is_superuser:
        return redirect(handle_login)
    
    if request.method == 'POST':
        image =''
        try:
            image = request.FILES['image']
            images = request.FILES.getlist('images')
        except:
            if image =='':
                messages.info(request,"Image field can't be empty")
                return redirect(add_product)
        name = request.POST['name']
        slug = request.POST['slug']
        brand = request.POST['brand']
        categor = request.POST['category']
        description = request.POST['desc']
       
        try:
             product.objects.get(product_name = name)
        except:
                check = [name,slug,description]
                for values in check:
                    if values == '':
                        messages.info(request,'some fields are empty')
                        return redirect(add_product)
                    else:
                        pass    
                brand_instance = Brand.objects.get(id=brand)
                category_instance = AdminCategory.objects.get(id=categor)

                product.objects.create(
                    product_name=name,
                    brand=brand_instance,
                    category=category_instance,
                    product_desc=description,
                    image=image,
                    slug=slug
                ).save()
                pr = product.objects.get(product_name = name)
                for image in images:
                    Productimage.objects.create(product=pr, pr_images=image)
               
                messages.info(request,f'product {name} created succefully')
                return redirect(add_product)
        else:
            messages.error(request,f'product "{name}" already exist')
            return redirect(add_product)

    brands = Brand.objects.all()
    categories = AdminCategory.objects.all()

    context = {
        'categories' : categories,
        'brands' : brands,
    }
    return render(request, 'adminpanel/page-form-product-1.html', context)

@login_required(login_url='handle_login')
def edit_product(request, id):
    if not request.user.is_superuser:
        return redirect(handle_login)
    if request.method == "POST":
        image = ''
        try:
            image = request.FILES['image']
            images = request.FILES.getlist('images')
            print(image)
            product_instance = product.objects.filter(id=id).first()
            product_instance.image = image
            product_instance.save()
        except KeyError:
            print('Hi')

        name = request.POST['name']
        slug = request.POST['slug']
        brand = request.POST['brand']
        category = request.POST['category']
        # price = request.POST['price']
        # stock = request.POST['stock']

        if name == '':
            messages.error(request, "Product name can't be null")
            return redirect(edit_product)

        brand_instance = Brand.objects.get(id=brand)
        category_instance = AdminCategory.objects.get(id=category)

        product_updated = product.objects.filter(id=id).update(
            product_name=name,
            brand=brand_instance,
            category=category_instance,
            slug=slug,
            # stock=stock,
            # price=price,
        )   

        messages.success(request, f'{name} updated successfully')
        return redirect('products')  # Replace 'products' with the correct URL name for the product listing page

    product_instance = product.objects.get(id=id)
    brands = Brand.objects.all()
    categories = AdminCategory.objects.all()
    context = {
        "product": product_instance,
        'categories': categories,
        'brands': brands,
    }

    return render(request, "adminpanel/product-update.html", context)

@login_required(login_url='handle_login')
def delete_product(request, id):
    if not request.user.is_superuser:
        return redirect(handle_login)
    # Rename the model class to Product (uppercase)
    product_instance = product.objects.get(id=id)  # Use lowercase for the variable name

    name = product_instance.product_name
    product_instance.is_available = False
    product_instance.save()    
    messages.success(request, f'Product "{name}" deleted')
    return redirect(products)



# add variant...............
@login_required(login_url='handle_login')
def variant(request):
    if not request.user.is_superuser:
        return redirect(handle_login)
    variant = ProductVariant.objects.all()
    context={
        'variant':variant
    }
    return render(request,'adminpanel/variant.html',context)
@login_required(login_url='handle_login')
def addvariant(request, id):
    if not request.user.is_superuser:
        return redirect(handle_login)   
    pr = product.objects.get(id=id)
    if request.method == 'POST':
        quantity = request.POST['quantity']
        price = request.POST['price']
        ram = request.POST['ram']
        storage=request.POST['storage']
        
        ProductVariant.objects.create(
            quantity = quantity,
            price = price,
            ram = ram,
            storage = storage,
            product=pr,
        ).save()
        messages.success(request, 'variant added')
    
    
        
    return render(request, 'adminpanel/addvariant.html', {'product' : pr})
        
# category section...


def add_category(request):
    if request.method == 'POST':
        # image = request.FILES.get('image', None)
        # if not image:
        #     messages.info(request, "Image field can't be empty")
        #     return redirect('add_category')
            
        name = request.POST.get('name')
        slug = request.POST.get('slug', '')
        description = request.POST.get('decs',)
       
        
        # Check if required fields are not empty
        if not all([name, slug]):
            messages.info(request, 'Some fields are empty')
            return redirect('add_category')

        try:
            AdminCategory.objects.get(category_name=name)
            messages.error(request, f'Category "{name}" already exists')
        except AdminCategory.DoesNotExist:
            # Create the new category instance
            category_instance = AdminCategory.objects.create(
                category_name=name,
                slug=slug,
                category_decs=description,
                # cat_img=image,
                
            )
            category_instance.is_available = True
            category_instance.save()
            messages.success(request, f'Category "{name}" successfully added')

    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_dashboard')

    categories = AdminCategory.objects.filter(is_available=True)
    context = {
        'categories': categories,
    }
    return render(request, 'adminpanel/page-categories.html', context)

def edit_category(request, id):
    if request.method == "POST":
        name = request.POST['name']
        slug = request.POST['slug']
        description = request.POST['desc']

        category = AdminCategory.objects.filter(id=id).update(
            category_name=name,
            slug=slug,
            category_decs=description,
        )
        messages.success(request,f'{name} updated successfully')
        return redirect(add_category)

    category = AdminCategory.objects.get(id=id)
    context = {
        'category' : category,
    }
    return render(request, "adminpanel/update-category.html", context)


def delete_category(request, id):
    category = AdminCategory.objects.get(id=id)
    name = category.category_name
    category.is_available = False
    category.save()
    messages.success(request,f'Category "{name}" deleted')
    return redirect(add_category)

# brand section-----
def add_brand(request):
    if request.method == "POST":
        name = request.POST['name']
        desc = request.POST['desc']

        brand = Brand.objects.create(
            brand_name = name,
            brand_desc = desc,
        )
        brand.save()
        messages.success(request,f'Brand "{name}" created')
        return redirect(add_brand)
    brand = Brand.objects.all()
    context = {
        'brands' : brand,
    }
    return render(request,"adminpanel/brand.html", context)

def edit_brand(request, id):
    brand = Brand.objects.get(id=id)
    if request.method == "POST":
        name = request.POST['name']
        desc = request.POST['desc']
        Brand.objects.filter(id=id).update(
            brand_name = name,
            brand_desc = desc,
        )
        messages.success(request,f'{name} updated successfully')
        return redirect(add_brand)
    return render(request, 'adminpanel/editbrand.html', {'brand':brand,})
# def delete_brand(request,id):
#     brand = Brand.objects.get(id=id)
#     name = Brand.brand_name
#     brand.is_available = False
#     brand.save()
#     messages.success(request,f'Brand "{name}" deleted')
#     return redirect(add_brand)