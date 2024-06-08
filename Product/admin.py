from collections.abc import Sequence
from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from .models import Products,SocialMediaTag
from .models import Collection



# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display=("product_name","product_price","product_sizes","collection")
    list_filter=("product_gender","prod_is_featured","collection_id")
    search_fields=("product_name__icontains",)
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

    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(collection=request.user.collection)

    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "collection":
            if request.user.is_superuser:
                kwargs["queryset"] = Collection.objects.all()
            else:
                kwargs["queryset"] = Collection.objects.filter(collection_name=request.user.collection)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

    def get_list_filter(self, request: HttpRequest):
        filter=super().get_list_filter(request)
        if request.user.is_superuser:
            return filter 
        filter=list(filter)
        filter.remove("collection_id")
        return tuple(filter)
    

        
    
admin.site.register(Products,ProductAdmin)
admin.site.register(SocialMediaTag)