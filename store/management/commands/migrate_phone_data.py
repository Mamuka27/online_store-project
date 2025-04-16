from django.core.management.base import BaseCommand
from store.models import Item
from store.tech_models.phone_models import PhoneSpecs

class Command(BaseCommand):
    help = "Migrate phone-related fields from Item to PhoneSpecs"

    def handle(self, *args, **options):
        phones = Item.objects.filter(subcategory__name__iexact='phones')

        for item in phones:
            try:
                PhoneSpecs.objects.create(
                    item=item,
                    screen_size=getattr(item, "screen_size", None),
                    resolution=getattr(item, "resolution", ""),
                    ram=getattr(item, "ram", None),
                    storage=getattr(item, "storage", None),
                    operating_system=getattr(item, "operating_system", ""),
                    battery_capacity=getattr(item, "battery_capacity", None),
                    fast_charging=getattr(item, "fast_charging", False),
                    sim_support=getattr(item, "sim_support", False),
                    touchscreen=getattr(item, "touchscreen", False),
                    bluetooth=getattr(item, "bluetooth", False),
                    wifi=getattr(item, "wifi", False),
                )
                self.stdout.write(self.style.SUCCESS(f"Migrated: {item.name}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error on {item.name}: {str(e)}"))
