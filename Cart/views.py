from django.http import JsonResponse
from django.shortcuts import redirect, render
from Product.models import Products
from .models import Cart,CartItems
import json
import uuid




def cart_page(request):
    return render(request,'cart/cart.html')

def delete_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user,paid=False)
        cart.delete()
    else:
        cart = Cart.objects.get(session_id=request.session.get('session_id'),paid=False)
        cart.delete()
    previous_page=request.META.get('HTTP_REFERER')
    return redirect(previous_page)


def add_to_cart(request):
    data=json.loads(request.body)
    product_id=data['id']
    product=Products.objects.get(id=product_id)
    user=request.user
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user,paid=False)
    else:
        try:
            session=request.session['session_id']
        except:
            session=request.session['session_id']=str(uuid.uuid4)
        cart, created = Cart.objects.get_or_create(session_id=session,paid=False)
    cart_item, created=CartItems.objects.get_or_create(cart=cart,product=product)
    cart_item.quantity+=1
    cart_item.save()
    response={"num_of_cart_items":cart.num_of_item,"item_qty":cart_item.quantity,
              "total_cart_sum":cart.total_cart_sum,"item_prod_id":cart_item.product.pk}
    return JsonResponse(response)
    # return JsonResponse(cart.num_of_item,safe=False)

def rm_from_cart(request):
    data=json.loads(request.body)
    product_id=data['id']
    product=Products.objects.get(id=product_id)
    user=request.user
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user,paid=False)
        
    else:
        try:
            session=request.session['session_id']
        except:
            session=request.session['session_id']=str(uuid.uuid4)
        cart, created = Cart.objects.get_or_create(session_id=session,paid=False)
        
    cart_item, created=CartItems.objects.get_or_create(cart=cart,product=product)
    cart_item.quantity-=1
    if cart_item.quantity < 1:
        cart_item.delete()
    else:
        cart_item.save()
    response={"num_of_cart_items":cart.num_of_item,"item_qty":cart_item.quantity,
              "total_cart_sum":cart.total_cart_sum,"item_prod_id":cart_item.product.pk }
    return JsonResponse(response)   
    # return JsonResponse(cart.num_of_item,safe=False)


def favourite_page(request):
    return render(request,'product/favourite.html')
