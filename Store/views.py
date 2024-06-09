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
    all_product=cache.get_or_set("all_product", Products.objects.all(), CACHE_TIMEOUT).order_by('-id')
    
    all_adds=cache.get_or_set("all_adds", Advertisement.objects.all(), CACHE_TIMEOUT).order_by('id')
    tags=cache.get_or_set("tags", SocialMediaTag.objects.all(), CACHE_TIMEOUT).order_by('-id')
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
    collection_prods=Products.objects.filter(collection_id=brand.id).order_by('-id')

    paginator = Paginator(collection_prods, 8)  # Show 8 products per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,"store/collection.html",{"page_obj": page_obj,'design_brand':brand})


def whats_hot_page(request):
    # all_products=Products.objects.all().order_by("-id")
    all_products=cache.get_or_set("all_products",Products.objects.all().order_by("-id"), CACHE_TIMEOUT)
    
    # advert=Advertisement.objects.get(advert_location="whats_hot_advert")
    advert=cache.get_or_set("advert",Advertisement.objects.get(advert_location="whats-hot_advert"), CACHE_TIMEOUT)
    paginator = Paginator(all_products, 10)  # Show 10 products per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,"store/whats-hot.html",{"page_obj": page_obj,"advert":advert})

def shop_all_page(request,category):
    filter_option=["All","Shirt","Polo","Trouser","Skirt","Gown","Suit","Sweater","Jump-Suit","Native","jacket"]
    if category=="All":
        # products=Products.objects.all().order_by("-id")
        products=cache.get_or_set("products",Products.objects.all().order_by("-id"), CACHE_TIMEOUT)
    else:
        products=Products.objects.filter(product_name__icontains=category)
    paginator = Paginator(products, 12)  # Show 8 products per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,"store/shop-all.html",{'page_obj':page_obj,"search_query":category.title(),"filter_option":filter_option})


def featured_prod_page(request):
    # all_featured=Products.objects.filter(prod_is_featured=True)
    all_featured=cache.get_or_set("all_featured",Products.objects.filter(prod_is_featured=True).order_by("-id"), CACHE_TIMEOUT)
    paginator = Paginator(all_featured, 12)  # Show 10 products per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'store/shop-all.html',{"page_obj":page_obj,"featured":True})

def category_page(request,category):
    category_options={"All":'Accessories',"Bags":"Bag","Glasses":"Glass","Shoes":"Shoe","Watches":"Watch","Sandals":"Sandal","Bangles":"Bangle","Perfumes":"Perfume"}
    if category=='All':
        category='accessories'
    products=Products.objects.filter(product_gender=category.upper()).order_by("-id")
    paginator = Paginator(products, 12)  # Show 10 products per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if category=="female" or category=="kids":
        return render(request,'store/female-category.html',{"page_obj":page_obj,category.upper():True})
    elif category=="male":
        return render(request,"store/male-category.html",{"page_obj":page_obj})
    elif category=="accessories" or category=="All":
        category='All'
        return render(request,"store/accessory-category.html",{"page_obj":page_obj,"query":category,'category_options':category_options})
    else:  
        products=Products.objects.filter(product_gender="ACCESSORIES",product_name__icontains=category_options[category]).order_by("-id")
        paginator = Paginator(products, 12)  # Show 10 products per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request,"store/accessory-category.html",{"page_obj":page_obj,"query":category,'category_options':category_options})



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


def collections_page(request):
    return render(request,'store/collections-page.html')

