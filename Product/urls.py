from django.urls import path
from . import views


urlpatterns = [
    path("search/", views.search_product, name="search-prod-page"  ),
    path("cart/", views.cart_page, name="cart-page"  ),
    path("favourite/", views.favourite_page, name="favourite-page"  ),
    path("<str:prod_name>/", views.single_product, name="single-prod-page"  ),

        
]