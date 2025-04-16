from django.urls import path
from django.views.generic import RedirectView
from store.views import (
    HomeView, ItemListView, ItemDetailView,
    AddToCartView, CartDetailView, UpdateCartView, RemoveFromCartView,
    AddReviewView, AddToWishlistView, RemoveFromWishlistView, WishlistView,
    CartPaymentView, CompletePaymentView, UnsuccessfulPaymentView,
    DeleteCardView
)
from store.views import DownloadReceiptView
from .views import AccountProfileView
from .views import AdminDashboardView, AdminHeatmapView, ExportHeatmapCSVView
from .views import ExportHeatmapCSVView

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/heatmap/', AdminHeatmapView.as_view(), name='admin_heatmap'),
    path('dashboard/heatmap/export/', ExportHeatmapCSVView.as_view(), name='export_heatmap_csv'),
    path('', ItemListView.as_view(), name='item_list'),
    path('home/', HomeView.as_view(), name='home'),
    path('account/', AccountProfileView.as_view(), name='account_profile'),

    path("account/delete_card/<int:card_id>/", DeleteCardView.as_view(), name="delete_card"),

    path('dashboard/heatmap/export/', ExportHeatmapCSVView.as_view(), name='export_heatmap_csv'),

    path('item/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('item/<int:item_id>/review/', AddReviewView.as_view(), name='add_review'),

    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:item_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/update/<int:item_id>/', UpdateCartView.as_view(), name='update_cart'),
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/payment/', CartPaymentView.as_view(), name='cart_payment'),
    path('cart/complete/', CompletePaymentView.as_view(), name='complete_payment'),
    path('cart/unsuccessful/', UnsuccessfulPaymentView.as_view(), name='unsuccessful_payment'),

    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/add/<int:item_id>/', AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),

    path('complete_payment/', CompletePaymentView.as_view(), name='complete_payment'),
    path('download_receipt/<str:code>/', DownloadReceiptView.as_view(), name='download_receipt'),
    path('login/', RedirectView.as_view(url='/accounts/login/')),
]



