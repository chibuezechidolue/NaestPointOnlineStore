from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_page, name="home-page"  ),
    path("collection/<str:collection_name>/", views.collection_page, name='collection-page'),
    path("new-arrivals/", views.whats_hot_page, name='whats-hot-page'),   
    path("shop-all/<str:category>/", views.shop_all_page, name='shop-all-page'), 
    path("featured/", views.featured_prod_page, name='featured-prod-page'),   

    
]