from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from user.models import Profile
from .models import Item, PriceHistory
from django.db.models.signals import pre_save

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()






@receiver(pre_save, sender=Item)
def save_price_history(sender, instance, **kwargs):
    if instance.pk:
        old_price = Item.objects.get(pk=instance.pk).price
        if instance.price != old_price:
            PriceHistory.objects.create(item=instance, price=instance.price)
