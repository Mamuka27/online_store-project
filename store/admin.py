from django.contrib import admin
from .models import (
    Category, SubCategory, Brand, Item, Review,
    CartItem, WishlistItem, ItemImage, PriceHistory
)
from .tech_models.phone_models import PhoneSpecs
from .tech_models.laptop_models import LaptopSpecs
from .tech_models.tv_models import TVSpecs
from .tech_models.tablet_models import TabletSpecs


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


class PhoneSpecsInline(admin.StackedInline):
    model = PhoneSpecs
    can_delete = False
    max_num = 1


class LaptopSpecsInline(admin.StackedInline):
    model = LaptopSpecs
    can_delete = False
    max_num = 1


class TVSpecsInline(admin.StackedInline):
    model = TVSpecs
    can_delete = False
    max_num = 1


class TabletSpecsInline(admin.StackedInline):
    model = TabletSpecs
    can_delete = False
    max_num = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcategory', 'get_category', 'brand', 'price', 'stock', 'is_available']
    list_filter = ['is_available', 'brand', 'subcategory']
    search_fields = ['name', 'subcategory__name', 'brand__name']
    prepopulated_fields = {'slug': ('name',)}

    def get_category(self, obj):
        return obj.subcategory.category.name
    get_category.short_description = 'Category'

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj)
        if obj and obj.subcategory:
            sub_slug = obj.subcategory.slug.lower()
            if "phone" in sub_slug:
                inlines.append(PhoneSpecsInline(self.model, self.admin_site))
            elif "laptop" in sub_slug:
                inlines.append(LaptopSpecsInline(self.model, self.admin_site))
            elif "tv" in sub_slug:
                inlines.append(TVSpecsInline(self.model, self.admin_site))
            elif "tablet" in sub_slug:
                inlines.append(TabletSpecsInline(self.model, self.admin_site))
        inlines.append(ItemImageInline(self.model, self.admin_site))
        inlines.append(PriceHistoryInline(self.model, self.admin_site))
        return inlines


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


@admin.register(PhoneSpecs)
class PhoneSpecsAdmin(admin.ModelAdmin):
    list_display = ('item', 'screen_size', 'ram', 'storage', 'battery_capacity')


@admin.register(LaptopSpecs)
class LaptopSpecsAdmin(admin.ModelAdmin):
    list_display = ('item', 'processor', 'ram', 'storage', 'screen_size')


@admin.register(TVSpecs)
class TVSpecsAdmin(admin.ModelAdmin):
    list_display = ('item', 'screen_size', 'resolution', 'smart_tv', 'hdmi_ports')


@admin.register(TabletSpecs)
class TabletSpecsAdmin(admin.ModelAdmin):
    list_display = ('item', 'screen_size', 'ram', 'storage', 'battery_capacity')
