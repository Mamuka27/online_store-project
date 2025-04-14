from django.contrib import admin
from .models import (
    Category, SubCategory, Brand, Item, Review,
    CartItem, WishlistItem, ItemImage, PriceHistory
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'category__name')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1
    fields = ['image', 'alt_text']
    max_num = 10


class PriceHistoryInline(admin.TabularInline):
    model = PriceHistory
    extra = 0
    readonly_fields = ('price', 'date')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcategory', 'get_category', 'brand', 'price', 'stock', 'is_available']
    list_filter = ['is_available', 'brand', 'subcategory']
    search_fields = ['name', 'subcategory__name', 'brand__name']
    prepopulated_fields = {'slug': ('name',)} 
    inlines = [ItemImageInline, PriceHistoryInline]

    def get_category(self, obj):
        return obj.subcategory.category.name
    get_category.short_description = 'Category'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'rating', 'verified_purchase', 'created_at')
    list_filter = ('verified_purchase', 'rating')
    search_fields = ('item__name', 'user__username')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity', 'added_at')
    search_fields = ('user__username', 'item__name')


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'added_at')
    search_fields = ('user__username', 'item__name')
