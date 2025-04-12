# store/cart.py

from decimal import Decimal
from django.conf import settings
from store.models import Item
from django.utils import timezone


class Cart:
    def __init__(self, request) -> None:
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, item: Item, quantity: int = 1, update_quantity: bool = False) -> None:
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {
                'quantity': 0,
                'price': str(item.price)
            }
        if update_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
        self.save()

    def save(self) -> None:
        self.session.modified = True

    def remove(self, item: Item) -> None:
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def clear(self) -> None:
        self.session[settings.CART_SESSION_ID] = {}
        self.save()

    def __iter__(self):
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)
        now = timezone.now()

        for item in items:
            cart_item = self.cart[str(item.id)]
            cart_item['item_obj'] = item

            # Choose the valid price: discount if available and valid
            if item.discount_price and item.discount_expiry and item.discount_expiry > now:
                price = item.discount_price
            else:
                price = item.price

            cart_item['price'] = Decimal(price)
            cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
            cart_item['unit_price'] = cart_item['price']
            yield cart_item

    def __len__(self) -> int:
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self) -> Decimal:
        total = Decimal('0')
        for cart_item in self:
            total += cart_item['total_price']
        return total
