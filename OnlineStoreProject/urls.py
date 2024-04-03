from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from Cart import views

admin.site.site_header="NAESTpoint Admin"
admin.site.site_title="NAESTpoint Administration"
admin.site.index_title="NAESTpoint Administration"



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Store.urls")),
    path("product/", include("Product.urls")),
    path("user/",include("User.urls")),
    path('cart/',include("Cart.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)