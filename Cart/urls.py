from django.urls import path
from . import views


urlpatterns = [
    path("view-cart", views.cart_page, name="cart-page"  ),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"  ),
    path("favourite/", views.favourite_page, name="favourite-page"  ),

]