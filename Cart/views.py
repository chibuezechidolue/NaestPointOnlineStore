from django.http import JsonResponse
from django.shortcuts import redirect, render
from Product.models import Products
from django.contrib.auth.decorators import login_required
from .models import Cart,CartItems, SavedItems
from django.contrib import messages
from django.db.utils import IntegrityError
import json
import uuid



def cart_page(request):
    return render(request,'cart/cart.html')

def delete_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user,paid=False)
        cart_items=cart.cartitems.all()
        cart_items.delete()
    else:
        cart = Cart.objects.get(session_id=request.session.get('session_id'),paid=False)
        cart_items=cart.cartitems.all()
        cart_items.delete()
    previous_page=request.META.get('HTTP_REFERER')
    return redirect(previous_page)


def add_to_cart(request):
    data=json.loads(request.body)
    product_id=data['id']
    product=Products.objects.get(id=product_id)
    user=request.user
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user,paid=False)
        saved_items=SavedItems.objects.filter(user=user)
        try:
            item=SavedItems.objects.get(product=product)
        except:
            item=product
        if item in saved_items:
            item.delete()
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
              "total_cart_sum":cart.total_cart_sum,"total_cart_sum_disc":cart.total_cart_sum_discount,
              "total_cart_sum_shipping_fee":cart.total_cart_sum_shipping_fee,"total_checkout_cost":cart.total_checkout_cost,
              "item_prod_id":cart_item.product.pk}
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
              "total_cart_sum":cart.total_cart_sum,"total_cart_sum_disc":cart.total_cart_sum_discount,
              "total_cart_sum_shipping_fee":cart.total_cart_sum_shipping_fee,
              "total_checkout_cost":cart.total_checkout_cost,"item_prod_id":cart_item.product.pk}
    return JsonResponse(response)   
    # return JsonResponse(cart.num_of_item,safe=False)


# def login_requirement(fn):
#     def wrapper(request,*args,**kwargs):
#         if request.user.is_anonymous:
#             messages.success(request,"Sorry! You are not logged in")
#             return redirect("login-page")
#         else:
#             return fn(request,*args,**kwargs)
#     return wrapper
# @login_requirement
@login_required
def favourite_page(request):
    return render(request,'cart/favourite.html')


def add_to_favourite(request):
    if not request.user.is_authenticated:
        return JsonResponse({"num_of_saved_items":"user_not_authenticated"})
    data=json.loads(request.body)
    product_id=data['id']
    prod=Products.objects.get(id=product_id)
    # try:
    item=SavedItems(user=request.user,product=prod)
    # except IntegrityError: 
    #     print("there was an integrity error")
    #     messages.add_message(request, messages.SUCCESS, "the Item is already in your favourites")
        
    usr_saved_items=SavedItems.objects.filter(user=request.user)
    item.save()
    num_of_item=len(usr_saved_items)
    response={"num_of_saved_items":num_of_item }
    return JsonResponse(response)


@login_required
def rm_from_favourite(request):
    data=json.loads(request.body)
    product_id=data['id']
    item=SavedItems.objects.get(user=request.user,product_id=product_id)
    usr_saved_items=SavedItems.objects.filter(user=request.user)
    item.delete()
    num_of_item=len(usr_saved_items)
    response={"num_of_saved_items":num_of_item}
    return JsonResponse(response)



@login_required
def delete_all_favourites(request):
    usr_saved_items=SavedItems.objects.filter(user=request.user)
    usr_saved_items.delete()
    messages.add_message(request, messages.SUCCESS, "All saved items has been deleted")
    previous_page=request.META.get('HTTP_REFERER')
    return redirect(previous_page)
