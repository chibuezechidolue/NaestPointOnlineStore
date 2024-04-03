from django.contrib import admin
from .models import Cart,CartItems
from django.utils.translation import gettext_lazy as _

# Register your models here.

class UserCartItemsFilter(admin.SimpleListFilter):
    title = _("user email")
    parameter_name = "user cart"
    def lookups(self, request, model_admin):
        # Example:
        # def lookups(self, request, model_admin):
        # countries = set([c.country for c in model_admin.model.objects.all()])
        # return [(c.id, c.name) for c in countries] + [
        #   ('AFRICA', 'AFRICA - ALL')]

        carts = set([cart_items.cart for cart_items in model_admin.model.objects.all()])
        return [(cart.id, cart.user.email) for cart in carts]
    
    def queryset(self, request, queryset):
        # to decide how to filter the queryset.
        # if self.value() == 'AFRICA':
        #     return queryset.filter(country__continent='Africa')
        #               OR
        if self.value():
            return queryset.filter(
                cart_id=self.value(),
                # paid=False,
            )


class CartItemAdmin(admin.ModelAdmin):
    list_display=("product","quantity",'cart','user')
    list_filter=(UserCartItemsFilter,'cart',"product",)
    # search_fields=("product.product_name__contains",)
    list_per_page=20
    # fields=("product_name","product_description","product_price",("product_img_1",'product_img_2','product_img_3'),"collection",("product_gender","prod_is_featured"))
    def user(self,obj):
        return obj.cart.user
    
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
class CartAdmin(admin.ModelAdmin):
    list_display=("user","paid",'date','view_cart_items',)
    list_filter=('user',"paid",)
    search_fields=("user__email__contains",)
    list_per_page=10
    actions=("set_cart_as_paid","set_cart_as_unpaid",)


    def view_cart_items(self,obj):
        # args=[obj.user_id]
        url=(reverse("admin:Cart_cartitems_changelist")+"?"+urlencode({"user cart":f"{obj.id}"}))
        return format_html("<a href='{}'>view items</a>",url)
    view_cart_items.short_description = 'view cart items'

    def set_cart_as_paid(self,request,queryset):
        queryset.update(paid=True)
        self.message_user(request, "The selected cart(s) has been set as paid")
    set_cart_as_paid.short_description="Set Selected Cart as Paid"

    def set_cart_as_unpaid(self,request,queryset):
        queryset.update(paid=False)
        self.message_user(request, "The selected cart(s) has been set as unpaid")
    set_cart_as_unpaid.short_description="Set Selected Cart as Not_Yet_Paid"

admin.site.register(Cart,CartAdmin)
admin.site.register(CartItems,CartItemAdmin)
