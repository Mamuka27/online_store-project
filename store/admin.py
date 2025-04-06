from django.contrib import admin
from .models import Item, Category, SubCategory, Brand, CartItem, WishlistItem, Review

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'subcategory', 'brand', 'is_available')
    list_filter = ('category', 'brand', 'is_available')
    search_fields = ('name',)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(CartItem)
admin.site.register(WishlistItem)
admin.site.register(Review)
