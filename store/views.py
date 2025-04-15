import os
import random
import string
from datetime import datetime
from django.db.models import Count, Q
from fpdf import FPDF

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Case, When, F, DecimalField, Count
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import now
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from .forms import ReviewForm
from .models import (
    Item, WishlistItem, Category, SubCategory,
    Brand, CartItem, Review, SavedCard,
    Order, OrderItem,Order, OrderItem

)
from .pdf_utils import ReceiptGenerator


def get_card_type(card_number):
    if card_number.startswith("4"):
        return "visa"
    elif card_number.startswith("5"):
        return "mastercard"
    elif card_number.startswith("3"):
        return "amex"
    elif card_number.startswith("6"):
        return "discover"
    return "default"


class HomeView(View):
    def get(self, request):
        return render(request, 'store/home.html')


class ItemListView(ListView):
    model = Item
    template_name = 'store/item_list.html'
    context_object_name = 'items'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        now = timezone.now()

        category = self.request.GET.get("category")
        subcategory = self.request.GET.get("subcategory")
        brand = self.request.GET.get("brand")
        rating = self.request.GET.get("rating")
        search_query = self.request.GET.get("search")
        special = self.request.GET.get("special")
        sort_option = self.request.GET.get("sort_by")

        if category:
            queryset = queryset.filter(subcategory__category_id=category)
        if subcategory:
            queryset = queryset.filter(subcategory_id=subcategory)
        if brand:
            queryset = queryset.filter(brand_id=brand)
        if rating:
            try:
                rating = float(rating)
                queryset = queryset.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=rating)
            except ValueError:
                pass
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        if special == "new":
            week_ago = now - timezone.timedelta(days=7)
            queryset = queryset.filter(created_at__gte=week_ago)
        if special == "bestseller":
            queryset = queryset.filter(is_featured=True)
        if special == "in_stock":
            queryset = queryset.filter(stock__gt=0)
        if special == "wishlist" and self.request.user.is_authenticated:
            wishlist_ids = WishlistItem.objects.filter(user=self.request.user).values_list("item_id", flat=True)
            queryset = queryset.filter(id__in=wishlist_ids)

        queryset = queryset.annotate(
            effective_price=Case(
                When(discount_price__isnull=False, discount_expiry__gt=now, then=F('discount_price')),
                default=F('price'),
                output_field=DecimalField()
            )
        )

        if sort_option == 'price_asc':
            queryset = queryset.order_by('effective_price')
        elif sort_option == 'price_desc':
            queryset = queryset.order_by('-effective_price')
        elif sort_option == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort_option == 'name_desc':
            queryset = queryset.order_by('-name')
        elif sort_option == 'created_at_desc':
            queryset = queryset.order_by('-created_at')
        elif sort_option == 'created_at_asc':
            queryset = queryset.order_by('created_at')
        elif sort_option == 'rating_desc':
            queryset = queryset.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
        elif sort_option == 'sale_ending_soon':
            queryset = queryset.filter(discount_expiry__gte=now).order_by('discount_expiry')
        elif sort_option == 'stock_first':
            queryset = queryset.order_by('-stock')
        elif sort_option == 'stock_last':
            queryset = queryset.order_by('stock')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "categories": Category.objects.all(),
            "subcategories": SubCategory.objects.all(),
            "brands": Brand.objects.all(),
            "selected_category": self.request.GET.get("category", ""),
            "selected_subcategory": self.request.GET.get("subcategory", ""),
            "selected_brand": self.request.GET.get("brand", ""),
            "rating": self.request.GET.get("rating", ""),
            "search_query": self.request.GET.get("search", ""),
            "selected_special": self.request.GET.get("special", ""),
            "selected_sort": self.request.GET.get("sort_by", ""),
            "now": timezone.now(),
        })
        if self.request.user.is_authenticated:
            context["wishlist_ids"] = WishlistItem.objects.filter(user=self.request.user).values_list("item_id", flat=True)
        else:
            context["wishlist_ids"] = []
        return context



class ItemDetailView(DetailView):
    model = Item
    template_name = 'store/item_detail.html'

    def get_object(self, queryset=None):
        item = super().get_object(queryset)
        item.views += 1
        item.save(update_fields=["views"])
        return item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        now_time = now()


        history = item.price_history.order_by('date')
        context['price_labels'] = [h.date.strftime('%Y-%m-%d') for h in history]
        context['price_values'] = [float(h.price) for h in history]
        context['discount_values'] = [float(h.discount_price) if h.discount_price else None for h in history]
        context['now'] = now_time


        base_qs = Item.objects.exclude(id=item.id)

        recommended_items = (
            base_qs
            .filter(
                Q(subcategory=item.subcategory) |
                Q(discount_expiry__gt=now_time) |
                Q(stock__gt=5)
            )
            .annotate(
                wishlist_count=Count("wishlist_items"),
                review_count=Count("reviews")
            )
            .order_by(
                '-wishlist_count',
                '-review_count',
                '-views',
                '-discount_price'
            )[:12] 
        )

        context["recommended_items"] = recommended_items

        reviews = item.reviews.all()
        context['reviews'] = reviews
        if reviews.exists():
            total = sum([r.rating for r in reviews])
            context['average_rating'] = round(total / reviews.count(), 1)
        else:
            context['average_rating'] = None

        context['review_form'] = ReviewForm()
        return context





class WishlistView(LoginRequiredMixin, View):
    def get(self, request):
        wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('item')
        return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items, 'now': now()})


class AddToWishlistView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        WishlistItem.objects.get_or_create(user=request.user, item=item)
        return redirect(request.META.get('HTTP_REFERER', 'item_list'))


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        WishlistItem.objects.filter(user=request.user, item=item).delete()
        return redirect(request.META.get('HTTP_REFERER', 'item_list'))


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        if item.stock <= 0:
            messages.error(request, f"Sorry, '{item.name}' is out of stock.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        quantity = int(request.POST.get("quantity", 1))
        cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
        current_qty = cart_item.quantity if not created else 0
        total_qty = current_qty + quantity

        if total_qty > item.stock:
            messages.error(request, f"Sorry, only {item.stock} unit(s) available.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        cart_item.quantity = total_qty
        cart_item.save()
        return redirect(request.META.get("HTTP_REFERER", "/"))


class CartDetailView(LoginRequiredMixin, View):
    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        valid_cart_items, total_price = [], 0

        for cart_item in cart_items:
            item = cart_item.item
            if item:
                unit_price = item.discount_price if item.discount_price and item.discount_expiry and item.discount_expiry > now() else item.price
                subtotal = unit_price * cart_item.quantity
                total_price += subtotal
                cart_item.unit_price = unit_price
                cart_item.subtotal = subtotal
                valid_cart_items.append(cart_item)
            else:
                cart_item.delete()

        return render(request, "store/cart_detail.html", {
            "cart_items": valid_cart_items,
            "total_price": total_price,
            "now": now(),
        })


class UpdateCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
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


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        CartItem.objects.filter(user=request.user, item=item).delete()
        return redirect('cart_detail')






class CartPaymentView(LoginRequiredMixin, View):
    def get(self, request):
        cards = SavedCard.objects.filter(user=request.user)
        saved_cards = [{"card": card, "type": get_card_type(card.card_number)} for card in cards]
        return render(request, "store/payment.html", {"saved_cards": saved_cards})

    def post(self, request):
        selected_card_id = request.POST.get("selected_card")
        card = None

        if selected_card_id:
            card = SavedCard.objects.filter(id=selected_card_id, user=request.user).first()
        else:
            card_number = request.POST.get("card_number", "").strip().replace(" ", "")
            expiry_date = request.POST.get("expiry_date", "").strip()
            cvv = request.POST.get("cvv", "").strip()
            cardholder_name = request.POST.get("card_name", "").strip()
            save_card = request.POST.get("save_card") == "on"


            if len(card_number) != 16 or not card_number.isdigit():
                messages.error(request, "❌ Card number must be exactly 16 digits.")
                return redirect("unsuccessful_payment")

            if len(cvv) != 3 or not cvv.isdigit():
                messages.error(request, "❌ CVV must be exactly 3 digits.")
                return redirect("unsuccessful_payment")


            if not self.is_valid_expiry(expiry_date):
                messages.error(request, "❌ This card has expired.")
                return redirect("unsuccessful_payment")

            if save_card and all([card_number, expiry_date, cvv, cardholder_name]):
                card = SavedCard.objects.create(
                    user=request.user,
                    card_number=card_number,
                    expiry_date=expiry_date,
                    cvv=cvv,
                    cardholder_name=cardholder_name
                )

        if card and not self.is_valid_expiry(card.expiry_date):
            messages.error(request, "❌ This card has expired.")
            return redirect("unsuccessful_payment")

        return redirect("complete_payment")

    def is_valid_expiry(self, expiry):
        try:
            month, year = map(int, expiry.split("/"))
            now_date = datetime.now()
            full_year = 2000 + year if year < 100 else year
            return full_year > now_date.year or (full_year == now_date.year and month >= now_date.month)
        except:
            return False

class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
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
        return redirect('item_detail', pk=item.id)


class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'store/register.html'
    success_url = reverse_lazy('login')



class AccountProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
        for order in recent_orders:
            order.order_items = OrderItem.objects.filter(order=order)

        wishlist_items = WishlistItem.objects.filter(user=user).select_related('item')
        cards = SavedCard.objects.filter(user=user)
        saved_cards = [{"card": card, "type": get_card_type(card.card_number)} for card in cards]

        context.update({
            'user': user,
            'recent_orders': recent_orders,
            'wishlist_items': [w.item for w in wishlist_items],
            'saved_cards': saved_cards,
        })
        return context
    
    

class DeleteCardView(LoginRequiredMixin, View):
    def post(self, request, card_id):
        card = get_object_or_404(SavedCard, id=card_id, user=request.user)
        card.delete()
        messages.success(request, "Card deleted.")
        return redirect("account_profile")


class UnsuccessfulPaymentView(LoginRequiredMixin, TemplateView):
    template_name = "store/unsuccessful_payment.html"


class DownloadReceiptView(LoginRequiredMixin, View):
    def get(self, request, code):
        file_path = f"media/receipts/receipt_{code}.pdf"
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        messages.error(request, "Receipt not found.")
        return redirect("account_profile")


class CompletePaymentView(LoginRequiredMixin, TemplateView):
    template_name = "store/payment_complete.html"

    def get(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            messages.warning(request, "No items to complete payment.")
            return redirect("cart_detail")

        total = 0
        order = Order.objects.create(user=request.user, total_amount=0)

        for cart_item in cart_items:
            item = cart_item.item
            quantity = cart_item.quantity or 0


            price = item.discount_price if item.discount_price and item.discount_expiry and item.discount_expiry > timezone.now() else item.price


            if price is None or quantity <= 0:
                continue 

            if item.stock >= quantity:

                item.stock -= quantity
                item.lifetime_sales += quantity
                item.save()


                total += price * quantity

                OrderItem.objects.create(
                    order=order,
                    item=item,
                    quantity=quantity,
                    price=price
                )
            else:
                messages.warning(request, f"Insufficient stock for {item.name}. Skipped.")

        if total == 0:
            order.delete()
            messages.error(request, "No valid items were processed.")
            return redirect("cart_detail")

        order.total_amount = total
        order.save()

        receipt_generator = ReceiptGenerator(order)
        receipt_generator.generate()

        cart_items.delete()

        return render(request, self.template_name, {
            "order": order,
            "pdf_url": f"/download_receipt/{receipt_generator.code}/"
        })


class CheckReceiptView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "store/check_receipt.html")

    def post(self, request):
        code = request.POST.get("receipt_code", "").strip().upper()
        pdf_path = f"media/receipts/receipt_{code}.pdf"

        if os.path.exists(pdf_path):
            latest_order = Order.objects.filter(user=request.user).order_by('-created_at').first()
            saved_cards = SavedCard.objects.filter(user=request.user)
            return render(request, "store/check_receipt.html", {
                "found": True,
                "receipt_code": code,
                "order": latest_order,
                "saved_cards": saved_cards,
                "pdf_url": f"/download_receipt/{code}/"
            })

        messages.error(request, "Receipt not found.")
        return render(request, "store/check_receipt.html", {"found": False})
