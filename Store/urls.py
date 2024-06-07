from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_page, name="home-page"  ),
    path("collections/<str:collection_name>/", views.collection_page, name='collection-page'),
    path("collections/", views.collections_page, name='collections-page'),
    path("new-arrivals/", views.whats_hot_page, name='whats-hot-page'),   
    path("shop-all/<str:category>/", views.shop_all_page, name='shop-all-page'), 
    path("featured/", views.featured_prod_page, name='featured-prod-page'),
    path("category/<str:category>/", views.category_page, name='category-page'),
    path("category/accessories/<str:category>/", views.category_page, name='category-page-accessory'),
    path("about-us/", views.about_us_page, name='about-us-page'),
    path("contact-us/", views.contact_us_page, name='contact-us-page'),

    
]