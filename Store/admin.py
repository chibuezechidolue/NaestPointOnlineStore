from django.contrib import admin
from .models import Advertisement,Collection

# Register your models here.


class AdvertAdmin(admin.ModelAdmin):
    list_display=("advert_title","advert_location")


class CollectionAdmin(admin.ModelAdmin):
    list_display=("collection_name","id")
    search_fields=("collection_name__icontains",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(collection_name=request.user.collection)


admin.site.register(Advertisement,AdvertAdmin)
admin.site.register(Collection,CollectionAdmin)
