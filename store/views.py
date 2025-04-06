from decimal import Decimal, InvalidOperation
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import (
    Item, Category, SubCategory, Brand,
    CartItem, WishlistItem, Review
)
from .forms import CustomUserCreationForm, ReviewForm

def item_list(request):
    items = Item.objects.filter(is_available=True)
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    brand = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    rating = request.GET.get('rating')
    search_query = request.GET.get('search')

    if category:
        items = items.filter(category__id=category)
    if subcategory:
        items = items.filter(subcategory__id=subcategory)
    if brand:
        items = items.filter(brand__id=brand)
    if min_price:
        try:
            items = items.filter(price__gte=Decimal(min_price))
        except InvalidOperation:
            pass
    if max_price:
        try:
            items = items.filter(price__lte=Decimal(max_price))
        except InvalidOperation:
            pass
    if rating:
        try:
            rating_decimal = Decimal(rating)
            items = items.filter(average_rating__gte=rating_decimal)
        except InvalidOperation:
            pass
    if search_query:
        items = items.filter(name__icontains=search_query)

    context = {
        'items': items,
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
        'brands': Brand.objects.all(),
        'selected_category': request.GET.get('category', ''),
        'selected_subcategory': request.GET.get('subcategory', ''),
        'selected_brand': request.GET.get('brand', ''),
        'min_price': request.GET.get('min_price', ''),
        'max_price': request.GET.get('max_price', ''),
        'rating': request.GET.get('rating', ''),
        'search_query': request.GET.get('search', ''),
    }
    return render(request, 'store/item_list.html', context)

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    reviews = item.reviews.all()

    is_in_wishlist = False
    if request.user.is_authenticated:
        is_in_wishlist = WishlistItem.objects.filter(user=request.user, item=item).exists()

    context = {
        'item': item,
        'reviews': reviews,
        'review_form': ReviewForm(),
        'is_in_wishlist': is_in_wishlist,
    }
    return render(request, 'store/item_detail.html', context)

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    messages.success(request, f"{item.name} added to your cart.")
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.item.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'store/cart_detail.html', context)

@login_required
def update_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart_item = get_object_or_404(CartItem, user=request.user, item=item)

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    except ValueError:
        pass

    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    CartItem.objects.filter(user=request.user, item=item).delete()
    return redirect('cart_detail')

@login_required
def add_review(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.item = item
            review.verified_purchase = CartItem.objects.filter(user=request.user, item=item).exists()
            review.save()
            messages.success(request, "Your review has been submitted.")
        else:
            messages.error(request, "There was an error with your review.")
    return redirect('item_detail', item_id=item.id)

@login_required
def add_to_wishlist(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    WishlistItem.objects.get_or_create(user=request.user, item=item)
    return redirect('item_detail', item_id=item.id)

@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    WishlistItem.objects.filter(user=request.user, item=item).delete()
    return redirect('wishlist')

@login_required
def wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('item')
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('item_list')


class RegistrationView(CreateView):
    template_name = 'store/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
