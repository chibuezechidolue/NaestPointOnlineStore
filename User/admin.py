from django.contrib import admin
from .models import CustomUser,NewsLetterSubscribers,NewsLetters

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display=("email","phone_no","address")
    list_filter=("is_staff","is_active","last_login")
    search_fields=("username__icontains","first_name__icontains","last_name__icontains",)
    list_per_page=10
    # fields=("product_name","product_description","product_price",("product_img_1",'product_img_2','product_img_3'),"collection",("product_gender","prod_is_featured"))
    # actions=("set_prod_to_featured","set_prod_to_unfeatured")

class NewsLetterAdmin(admin.ModelAdmin):
    list_display=('subject','created_at')
    actions=['send_newsletter',]

    def send_newsletter(self, request, queryset):
        for newsletter in queryset:
            newsletter.send(request)
        self.message_user(request, "The selected newsletter(s) has been Sent")

    send_newsletter.short_description = "Send selected Newsletters to all subscribers"

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(NewsLetters,NewsLetterAdmin)
admin.site.register(NewsLetterSubscribers)
