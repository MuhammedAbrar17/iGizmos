from .models import AdminCategory

def menu_links(request):
    links = AdminCategory.objects.all()
    return dict(links = links)  
