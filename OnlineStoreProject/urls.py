from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from Cart import views
import Product.views 


admin.site.site_header="NaestPoint Administration"
admin.site.site_title="NaestPoint Administration"
admin.site.index_title="NaestPoint Admin"
admin.site.empty_value_display = "(None)"


urlpatterns = [
    path("admin/", admin.site.urls),
    path('FAQ/',Product.views.faq_page,name='faq-page'),
    path('size-guide/',Product.views.size_guide_page,name='size-guide'),
    path("", include("Store.urls")),
    path("product/", include("Product.urls")),
    path("user/",include("User.urls")),
    path('cart/',include("Cart.urls")),
    path("customer/favourite/wish-list", views.favourite_page, name="favourite-page" ),
    path("customer/favourite/wish-list/delete-all", views.delete_all_favourites, name="delete-all-fav" ),
    path("customer/add-to-favourite",views.add_to_favourite,name="add-to-favourite"),
    path("customer/rm-from-favourite",views.rm_from_favourite,name="rm-from-favourite"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)