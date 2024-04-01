from django.urls import path
from . import views


urlpatterns = [
    path("search/", views.search_product, name="search-prod-page"  ),
    path("<str:prod_name>/", views.single_product, name="single-prod-page"  ),

        
]