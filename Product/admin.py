from django.contrib import admin
from .models import Products


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display=("product_name","product_price","product_sizes")
    list_filter=("product_gender","prod_is_featured","collection_id")
    search_fields=("product_name__contains",)
    list_per_page=20
    fields=("product_name","product_description","product_price","product_sizes",("product_img_1",'product_img_2','product_img_3'),"collection",("product_gender","prod_is_featured"))
    actions=("set_prod_to_featured","set_prod_to_unfeatured")

    def set_prod_to_featured(self,request,queryset):
        queryset.update(prod_is_featured=True)
        self.message_user(request, "The selected product(s) has been Featured")
    set_prod_to_featured.short_description="Set Selected Product as Featured"


    def set_prod_to_unfeatured(self,request,queryset):
        queryset.update(prod_is_featured=False)
        self.message_user(request, "The selected product(s) has been Unfeatured")
    set_prod_to_unfeatured.short_description="Set Selected Product as Unfeatured"

admin.site.register(Products,ProductAdmin)
