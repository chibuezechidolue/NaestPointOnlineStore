from django.http import JsonResponse
from django.shortcuts import render
from Product.models import Products
from .models import Cart,CartItems
import json
import uuid




def cart_page(request):
    return render(request,'cart/cart.html')


def add_to_cart(request):
    data=json.loads(request.body)
    print(data)
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
    cartitem, created=CartItems.objects.get_or_create(cart=cart,product=product)
    cartitem.quantity+=1
    cartitem.save()

    return JsonResponse(cart.num_of_item,safe=False)

def rm_from_cart(request):
    data=json.loads(request.body)
    print(data)
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
        
    return JsonResponse(cart.num_of_item,safe=False)


def favourite_page(request):
    return render(request,'product/favourite.html')
