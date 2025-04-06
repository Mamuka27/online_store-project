from django.contrib import admin
from django.urls import path, include
from store import views as store_views
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', store_views.item_list, name='item_list'),
    path('item/<int:item_id>/', store_views.item_detail, name='item_detail'),
    path('add-to-cart/<int:item_id>/', store_views.add_to_cart, name='add_to_cart'),
    path('cart/', store_views.cart_detail, name='cart_detail'),
    path('update-cart/<int:item_id>/', store_views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', store_views.remove_from_cart, name='remove_from_cart'),
    path('add-review/<int:item_id>/', store_views.add_review, name='add_review'),
    path('add-to-wishlist/<int:item_id>/', store_views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:item_id>/', store_views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', store_views.wishlist, name='wishlist'),
    path('register/', store_views.RegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),



    # ✅ This enables login/logout/password views
    path('accounts/', include('django.contrib.auth.urls')),
]


from django.views.generic import RedirectView

urlpatterns += [
    path('login/', RedirectView.as_view(url='/accounts/login/')),
]
