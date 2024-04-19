from django.shortcuts import redirect, render
from Product.models import Products,SocialMediaTag
from .models import Advertisement, Collection
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.core.cache import cache
import os

CACHE_TIMEOUT=60*10

def home_page(request):
    all_product=cache.get_or_set("all_product", Products.objects.all(), CACHE_TIMEOUT)
    
    all_adds=cache.get_or_set("all_adds", Advertisement.objects.all(), CACHE_TIMEOUT)
    tags=cache.get_or_set("tags", SocialMediaTag.objects.all(), CACHE_TIMEOUT)
    # featured_prod=all_product.filter(prod_is_featured=True)
    # mens_product=all_product.filter(product_gender="MALE")
    context={'featured':all_product.filter(prod_is_featured=True),
               "mens_prod":all_product.filter(product_gender="MALE"),
               "carousel":all_adds.filter(advert_location="CAROUSEL"),
               "sec2_ads":all_adds.filter(advert_location="sec2_advert"),
               "sec3_ads":all_adds.filter(advert_location="sec3_advert"),
               "sec4_ads":all_adds.filter(advert_location="sec4_advert"),
               "tags":tags}
    
    return render(request,'store/index.html',context)


def collection_page(request,collection_name):
    brand=Collection.objects.get(collection_name=collection_name)
    collection_prods=Products.objects.filter(collection_id=brand.id)

    paginator = Paginator(collection_prods, 8)  # Show 8 products per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,"store/collection.html",{"page_obj": page_obj,'design_brand':brand})


def whats_hot_page(request):
    # all_products=Products.objects.all().order_by("-id")
    all_products=cache.get_or_set("all_products",Products.objects.all().order_by("-id"), CACHE_TIMEOUT)
    
    # advert=Advertisement.objects.get(advert_location="whats_hot_advert")
    advert=cache.get_or_set("advert",Advertisement.objects.get(advert_location="whats_hot_advert"), CACHE_TIMEOUT)
    paginator = Paginator(all_products, 10)  # Show 10 products per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,"store/whats-hot.html",{"page_obj": page_obj,"advert":advert})

def shop_all_page(request,category):
    if category=="all":
        # products=Products.objects.all().order_by("-id")
        products=cache.get_or_set("products",Products.objects.all().order_by("-id"), CACHE_TIMEOUT)
    else:
        products=Products.objects.filter(product_name__icontains=category)
    
    paginator = Paginator(products, 8)  # Show 8 products per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,"store/shop-all.html",{'page_obj':page_obj,"search_query":category.title()})


def featured_prod_page(request):
    # all_featured=Products.objects.filter(prod_is_featured=True)
    all_featured=cache.get_or_set("all_featured",Products.objects.filter(prod_is_featured=True), CACHE_TIMEOUT)
    paginator = Paginator(all_featured, 10)  # Show 10 products per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'store/shop-all.html',{"page_obj":page_obj,"featured":True})

def category_page(request,category):
    products=Products.objects.filter(product_gender=category)
    paginator = Paginator(products, 10)  # Show 10 products per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if category=="FEMALE" or category=="KIDS":
        return render(request,'store/female-category.html',{"page_obj":page_obj,category:True})
    elif category=="MALE":
        return render(request,"store/male-category.html",{"page_obj":page_obj})
    elif category=="ACCESSORIES":
        return render(request,"store/accessory-category.html",{"page_obj":page_obj,"query":category})
    else:  
        category_options={"BAGS":"Bag","GLASSES":"Glass","SHOES":"Shoe","WATCHES":"Watch","SANDALS":"Sandal","BANGLES":"Bangle"}
        products=Products.objects.filter(product_gender="ACCESSORIES",product_name__icontains=category_options[category])
        paginator = Paginator(products, 10)  # Show 10 products per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request,"store/accessory-category.html",{"page_obj":page_obj,"query":category})



def about_us_page(request):
    return render(request,'store/about-us.html')

def contact_us_page(request):
    if request.method=="POST":
        content = request.POST
        name=content.get('name')
        email=content['email']
        subject=content.get('email_subject')
        message=content.get('email_content')
        send_mail(
                subject='Message from NaestPoint Store',
                message=f"{subject}\n\nName: {name}\nEmail: {email}\nMessage: {message}",   
                from_email=None,
                recipient_list=[os.environ.get('EMAIL_USERNAME'),],  
            )
        messages.add_message(request, messages.SUCCESS, "Your message was sent successfully")
        # return redirect('home-page')
    return render(request,'store/contact-us.html')

