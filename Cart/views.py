from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.shortcuts import redirect, render
from dotenv import load_dotenv
from Product.models import Products
from django.contrib.auth.decorators import login_required
from .models import Cart,CartItems, SavedItems
from django.contrib import messages
from django.db.utils import IntegrityError
from django.urls import reverse
import json
import uuid
import requests
import os


load_dotenv()


def checkout_complete(request):
    status=request.GET.get('status', None)
    if status=="successful":
        tx_ref=request.GET.get('tx_ref', None)
        transaction_id=request.GET["transaction_id"]
        # reconfirm/verify transaction
        url=f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"    #verify by transcation_id(params not required)
        # url="https://api.flutterwave.com/v3/transactions/verify_by_reference"       #verify by tx-ref(params required)
        
        header={
                "Authorization": "Bearer " + os.environ.get("FLUTTER_API_KEY")
            }
        params={"tx_ref":tx_ref}
        response=requests.get(url=url,headers=header,params=params)
        response=response.json()
        cart_id=response['data']['meta']['cart_id']
        cart = Cart.objects.get(id=cart_id,paid=False)
        if response['data']['status'] == "successful" and response['data']['amount'] >= cart.total_checkout_cost[0] and response['data']['currency'] == "NGN":
            transaction_id=response['data'].get("id")
            cart.paid,cart.transaction_id,cart.tx_ref = True,transaction_id,tx_ref
            cart.save()
            return render(request,'cart/checkout-complete.html',{"order_id":cart_id})
    else:
        messages.add_message(request, messages.WARNING, "Transaction Failed!!!  Your payment was not successfull")
        return redirect('cart-page')


    

@login_required()
def checkout(request):
    if request.method=="POST":
        total_cost=request.POST.get("total_checkout_cost")
        cart = Cart.objects.get(user=request.user,paid=False)
        redirect_url=request.build_absolute_uri(reverse('checkout-complete-page'))
        
        url="https://api.flutterwave.com/v3/payments"
        header={
                "Authorization": "Bearer " + os.environ.get("FLUTTER_API_KEY")
            }
        data= {
                "tx_ref": str(uuid.uuid4()),
                "amount": total_cost,
                "currency": "NGN",
                "redirect_url": redirect_url,
                "meta": {
                    "consumer_id": request.user.pk,
                    # "consumer_mac": "92a3-912ba-1192a",
                    "cart_id":str(cart.id)
                },
                "customer": {
                    "email": request.user.email,
                    "phonenumber": request.user.phone_no,
                    "name": request.user.first_name
                },
                "customizations": {
                    'title': "NaestPoint Product Payment",
                    "logo": "https://nastpoints3bucket.s3.eu-north-1.amazonaws.com/static/images/NaestPoint-favicon.ico"
                },
                "configurations": {
                    "session_duration": 10, #Session timeout in minutes (maxValue: 1440 minutes)    
                    "max_retry_attempt": 1, #Max retry (int)
                }, 
            }
        

        try:
            response=requests.post(url=url,headers=header,json=data)
        except Exception as e:
            print(f"An error occured when fetching payment confirmation,this is the error: {e}")

        response=response.json()
        flutter_link=response["data"]["link"]
        return HttpResponseRedirect(flutter_link)




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
            session=request.session['session_id']=str(uuid.uuid4())
        cart, created = Cart.objects.get_or_create(session_id=session,paid=False)
    cart_item, created=CartItems.objects.get_or_create(cart=cart,product=product)
    cart_item.quantity+=1
    cart_item.save()
    response={"num_of_cart_items":cart.num_of_item,"item_qty":cart_item.quantity,
              "total_cart_sum":cart.total_cart_sum[1],"total_cart_sum_disc":cart.total_cart_sum_discount[1],
              "total_cart_sum_shipping_fee":cart.total_cart_sum_shipping_fee[1],"total_checkout_cost":cart.total_checkout_cost[1],
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
            session=request.session['session_id']=str(uuid.uuid4())
        cart, created = Cart.objects.get_or_create(session_id=session,paid=False)
        
    cart_item, created=CartItems.objects.get_or_create(cart=cart,product=product)
    cart_item.quantity-=1
    if cart_item.quantity < 1:
        cart_item.delete()
    else:
        cart_item.save()
    response={"num_of_cart_items":cart.num_of_item,"item_qty":cart_item.quantity,
              "total_cart_sum":cart.total_cart_sum[1],"total_cart_sum_disc":cart.total_cart_sum_discount[1],
              "total_cart_sum_shipping_fee":cart.total_cart_sum_shipping_fee[1],
              "total_checkout_cost":cart.total_checkout_cost[1],"item_prod_id":cart_item.product.pk}
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
    
    item=SavedItems(user=request.user,product=prod)
        
    usr_saved_items=SavedItems.objects.filter(user=request.user)
    try:
        item.save()
    except IntegrityError:
        return JsonResponse({"num_of_saved_items":"item_already_saved"})

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
