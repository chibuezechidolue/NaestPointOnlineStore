from django.shortcuts import render
from .models import Products
from django.core.paginator import Paginator
from django.views import generic


# Create your views here.

def single_product(request,prod_name):
    product=Products.objects.get(product_name=prod_name)
    prod_suggestions=Products.objects.filter(product_gender=product.product_gender)[:6]
    
    return render(request,'product/single-product.html',{"product":product,"prod_suggestions":prod_suggestions}) 

from django.core.cache import cache
from django.core.cache import caches

def search_product(request):
    if 'search_bar' in request.GET:
        search_input=request.GET.get('search_bar')
        products=Products.objects.filter(product_name__contains=search_input)
        paginator = Paginator(products, 8)  # Show 8 products per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context={'page_obj':page_obj,"search":True,"search_query":search_input}
        cache.set("products",products,30)
        cache.set("search_query",search_input,30)
    else:
        products=cache.get('products')
        paginator = Paginator(products, 8)  # Show 8 products per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context={"page_obj":page_obj,"search":True,"search_query":cache.get('search_query')}
        # context={'page_obj':page_obj,"search":True,"search_query":search_input}
    return render(request,"store/shop-all.html",context)
