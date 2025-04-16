from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from user.models import Profile
from .models import Item, PriceHistory
from .tech_models.phone_models import PhoneSpecs
from .tech_models.laptop_models import LaptopSpecs
from .tech_models.tv_models import TVSpecs
from .tech_models.tablet_models import TabletSpecs


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

@receiver(post_save, sender=Item)
def create_spec_models(sender, instance, created, **kwargs):
    if created and instance.subcategory:
        sub_slug = instance.subcategory.slug.lower()

        if 'phone' in sub_slug and not hasattr(instance, 'phonespecs'):
            PhoneSpecs.objects.create(item=instance)
        elif 'laptop' in sub_slug and not hasattr(instance, 'laptopspecs'):
            LaptopSpecs.objects.create(item=instance)
        elif 'tv' in sub_slug and not hasattr(instance, 'tvspecs'):
            TVSpecs.objects.create(item=instance)
        elif 'tablet' in sub_slug and not hasattr(instance, 'tabletspecs'):
            TabletSpecs.objects.create(item=instance)
