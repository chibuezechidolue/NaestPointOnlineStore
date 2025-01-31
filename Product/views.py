from django.shortcuts import render,redirect
from .models import Products
from django.core.paginator import Paginator
from django.views import generic
from django.core.cache import cache
from Cart.models import CartItems,Cart
from django.contrib import messages
import uuid




# Create your views here.
CACHE_TIMEOUT=60*10

def single_product(request,prod_name):
    product=Products.objects.get(product_name=prod_name)
    prod_suggestions=Products.objects.filter(product_gender=product.product_gender).order_by("-id")[:6]
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
        print(prod_size)
        prod_qty=request.POST.get('quantity')
        if int(prod_qty)<=0:
            messages.add_message(request, messages.WARNING, "Minimum quantity that can be added to cart is 1")
            previous_page=request.META.get('HTTP_REFERER')
            return redirect(previous_page)
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user,paid=False)
        else:
            try:
                session=request.session['session_id']
            except:
                session=request.session['session_id']=str(uuid.uuid4())
            cart, created = Cart.objects.get_or_create(session_id=session,paid=False)

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
        products=Products.objects.filter(product_name__icontains=search_input).order_by("-id")
        paginator = Paginator(products, 8)  # Show 8 products per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context={'page_obj':page_obj,"search":True,"search_query":search_input}
        if request.user.is_authenticated:
            cache.set(f"{request.user.email}_search_result",products,100)
            cache.set(f"{request.user.email}_search_query",search_input,100)
        else:
            cache.set(f"{request.session['session_id']}_search_result",products,100)
            cache.set(f"{request.session['session_id']}_search_query",search_input,100)
    else:
        if request.user.is_authenticated:
            products = cache.get(f"{request.user.email}_search_result")
            query_search=cache.get(f"{request.user.email}_search_query")
        else:
            products=cache.get(f"{request.session['session_id']}_search_result")
            query_search=cache.get(f"{request.session['session_id']}_search_query")
        # products=cache.get(f"{request.user.email}_search_result")
        paginator = Paginator(products, 8)  # Show 8 products per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context={"page_obj":page_obj,"search":True,"search_query":query_search}
    return render(request,"store/shop-all.html",context)


def faq_page(request):
    return render(request,"product/faq.html")

def size_guide_page(request):
    return render(request,'product/size-guide.html')