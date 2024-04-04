from django.shortcuts import render,redirect
from .models import Products
from django.core.paginator import Paginator
from django.views import generic
from django.core.cache import cache
from Cart.models import CartItems,Cart
from django.contrib import messages




# Create your views here.

def single_product(request,prod_name):
    product=Products.objects.get(product_name=prod_name)
    prod_suggestions=Products.objects.filter(product_gender=product.product_gender)[:6]
    # if request.user.is_authenticated:
    #     cart=Cart.objects.get(user=request.user,paid=False)
    # else:
    #     cart=Cart.objects.get(session_id=request.session['session_id'],paid=False)
    # try:
    #     item=CartItems.objects.get(cart=cart,product=product)
    #     item_qty=item.quantity
    # except:
    #     item_qty=0
    # context={"product":product,"prod_suggestions":prod_suggestions,"item_qty":item_qty}
    if request.method=="POST":
        prod_size=request.POST.get('size_choice')
        prod_qty=request.POST.get('quantity')
        if int(prod_qty)<=0:
            messages.add_message(request, messages.WARNING, "Minimum quantity that can be added to cart is 1")
            previous_page=request.META.get('HTTP_REFERER')
            return redirect(previous_page)
        if request.user.is_authenticated:
            cart=Cart.objects.get(user=request.user,paid=False)
        else:
            cart=Cart.objects.get(session_id=request.session['session_id'],paid=False)

        item=CartItems(cart=cart,product=product,quantity=prod_qty,size=prod_size)
        exist=False
        for prod in cart.cartitems.all():
            if item.product.product_name==prod.product.product_name:
                existing_item=prod
                existing_item.quantity=int(item.quantity)
                existing_item.save()
                exist=True
        if not exist:
            item.save()
        messages.add_message(request, messages.SUCCESS, "Item has been added to Cart")
        # previous_page=request.META.get('HTTP_REFERER')
        # return redirect(previous_page)
    
    try:
        item=CartItems.objects.get(cart=cart,product=product)
        item_qty=item.quantity
    except:
        item_qty=0
    context={"product":product,"prod_suggestions":prod_suggestions,"item_qty":item_qty}
    return render(request,'product/single-product.html',context) 


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


