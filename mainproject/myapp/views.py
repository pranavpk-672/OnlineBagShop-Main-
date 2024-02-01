from myauth.models import category
from django.shortcuts import render

from myauth.models import Product
from myauth.models import sub_category
#from django.views.decorators.cache import never_cache

# Create your views here.
#@never_cache
# def index(request):
#     return render(request,'index.html')


def index(request):
      
        items = Product.objects.all()[:12]
        categories = category.objects.all()
        subcategories = sub_category.objects.all()

        response = render(request, 'index.html', {'items': items,  
                                                 'categories': categories, 'subcategories': subcategories})
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
   