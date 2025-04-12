from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import random
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
def generate_slug(instance, value, prefix):

    generated = slugify(value)
    if not generated:
        generated = f"{prefix}-{random.randint(1000, 9999)}"
    return generated


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self, self.name, "cat")
        super(Category, self).save(*args, **kwargs)


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "SubCategories"

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self, self.name, "subcat")
        super(SubCategory, self).save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self, self.name, "brand")
        super(Brand, self).save(*args, **kwargs)





class PhoneInformation(models.Model):
    color = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    release_date = models.DateField()

    sim_type = models.CharField(max_length=50)
    esim = models.BooleanField()
    supports_5g = models.BooleanField()
    body_material = models.CharField(max_length=255)
    ip_rating = models.CharField(max_length=20)

    chipset = models.CharField(max_length=100)
    gpu = models.CharField(max_length=100)
    os = models.CharField(max_length=100)
    os_version = models.CharField(max_length=100)
    stereo_speakers = models.BooleanField()
    bluetooth_version = models.CharField(max_length=10)
    nfc = models.BooleanField()

    display_size = models.CharField(max_length=100)
    resolution = models.CharField(max_length=100)
    refresh_rate = models.CharField(max_length=50)
    brightness = models.CharField(max_length=50)
    display_type = models.CharField(max_length=100)
    screen_protection = models.CharField(max_length=100)

    internal_storage = models.CharField(max_length=50)
    storage_type = models.CharField(max_length=50)
    ram = models.CharField(max_length=50)
    microsd_slot = models.BooleanField()

    main_camera = models.TextField()
    additional_cameras = models.TextField()
    front_camera = models.TextField()
    main_video_resolution = models.CharField(max_length=100)
    front_video_resolution = models.CharField(max_length=100)

    headphone_jack = models.CharField(max_length=10)
    charging_port = models.CharField(max_length=50)

    battery_capacity = models.CharField(max_length=50)
    battery_type = models.CharField(max_length=50)
    wireless_charging = models.BooleanField()
    wireless_power = models.CharField(max_length=50)

    weight = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.brand} - {self.color}"
    
class Item(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    description = models.TextField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='items')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_expiry = models.DateTimeField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, editable=False)
    lifetime_sales = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_info = models.OneToOneField(PhoneInformation, null=True, blank=True, on_delete=models.SET_NULL)


    def current_price(self):

        if self.discount_price and self.discount_expiry and self.discount_expiry > timezone.now():
            return self.discount_price
        return self.price
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self, self.name, "item")
        super(Item, self).save(*args, **kwargs)

    def update_average_rating(self):
        avg = self.reviews.aggregate(average=Avg('rating'))['average']
        self.average_rating = avg if avg else 0.0
        self.save(update_fields=['average_rating'])

    @property
    def category(self):
        return self.subcategory.category


class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        username = self.user.username if self.user else 'Anonymous'
        return f"Review for {self.item.name} by {username}"


@receiver(post_save, sender=Review)
def update_item_rating_on_save(sender, instance, **kwargs):
    instance.item.update_average_rating()


@receiver(post_delete, sender=Review)
def update_item_rating_on_delete(sender, instance, **kwargs):
    instance.item.update_average_rating()






class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.item.name} (x{self.quantity}) in {self.user.username}'s cart"




class SavedCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_cards')
    card_number = models.CharField(max_length=32)

    expiry_date = models.CharField(max_length=5)  
    cvv = models.CharField(max_length=4)
    cardholder_name = models.CharField(max_length=100)
    added_at = models.DateTimeField(auto_now_add=True)

    def last4(self):
        return self.card_number[-4:]

    def __str__(self):
        return f"{self.user.username} - ****{self.last4()}"



class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='wishlist_items')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.item.name} in {self.user.username}'s wishlist"











class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Completed")

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

