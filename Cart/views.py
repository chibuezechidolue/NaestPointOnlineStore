from django.http import JsonResponse
from django.shortcuts import render
from Product.models import Products
from .models import Cart,CartItems
import json




def cart_page(request):
    user=request.user
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user,paid=False)
        cartitems,created=CartItems.objects.get_or_create(cart=cart)
    return render(request,'product/cart.html')


def add_to_cart(request):
    data=json.loads(request.body)
    product_id=data['id']
    print(product_id)
    products=Products.objects.get(id=id)
    return JsonResponse('it is working',safe=False)

def favourite_page(request):
    return render(request,'product/favourite.html')
