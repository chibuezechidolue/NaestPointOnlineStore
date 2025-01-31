from .models import Collection,Advertisement
from User.forms import NewsLetterForm
from Cart.models import Cart,CartItems, SavedItems
from django.core.cache import cache
from django.core.paginator import Paginator
import uuid




CACHE_TIMEOUT=60*10

form=NewsLetterForm()
def nav_bar(request):
    user=request.user
    if user.is_authenticated:
        try:
            cart = Cart.objects.get(user=user,paid=False)
        except:
            cart={"num_of_item":0}
        usr_saved_items= SavedItems.objects.filter(user=request.user)
    else:
        usr_saved_items=[]
        try:
            session=request.session['session_id']
        except:
            request.session['session_id']=str(uuid.uuid4())
            session=request.session.get('session_id')
        finally:
            try:
                cart = Cart.objects.get(session_id=session,paid=False)
            except:
                cart={"num_of_item":0}
    user_saved_items=[item.product for item in usr_saved_items]

    size_options=['SM','MD','LG','XL']
    collections=cache.get_or_set("collections", Collection.objects.all(), CACHE_TIMEOUT).order_by('id')[1:]
    collection_paginator = Paginator(collections, 10)  # Show 10 products per page.
    page_number = request.GET.get("page")
    collection_page_obj = collection_paginator.get_page(page_number)
    nav_advert=cache.get_or_set("nav_advert",Advertisement.objects.get(advert_location="Nav_advert"),CACHE_TIMEOUT)
    return {'collection_page_obj': collection_page_obj,
            "nav_advert":nav_advert,"newsletterform":form,
            "cart":cart,"saved_items":user_saved_items,
            "size_options":size_options
            }

